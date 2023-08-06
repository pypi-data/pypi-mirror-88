import json
import os
import sys
import platform
import threading
import traceback

from .api_call import api_call, api_auth
from .account import Account
from .user import User

__version__ = "1.0.6"


class FreedomClient(object):
    """Freedom Robotics API client library. Instantiate this first and access all API functions from within a FreedomClient.

    You can instantiate a `FreedomClient` using either no arguments (in which case credentials are searched for in ~/.freedom_credentials), a `token` and `secret`, or a `username` and `password`.

    Args:
        token (str): API token. Can be a session or user token.
        secret (str): API secret.
        username (str): Username.
        password (str): Password.
    """

    def __init__(self, token =None, secret =None, username=None, password=None, url=None):
        # if class is initialized with a token and secret, use it
        if token is not None and secret is not None:
            self.token = token
            self.secret = secret
            api_auth(self.token, self.secret, url=url)

        # if class is initialized with a username and password, use it
        elif username is not None and password is not None:
            response = api_call(
                "PUT", 
                "/users/{}/login".format(username),
                data={
                    "password": password
                },
                no_auth=True)
            self.token = response.get("token")
            self.secret = response.get("secret")
            api_auth(self.token, self.secret, url=url)

        # if there is a saved freedom credentials file, use it
        elif os.path.exists(os.path.expanduser("~/.freedom_credentials")):
            with open(os.path.expanduser("~/.freedom_credentials")) as f:
                credentials = json.load(f)
                if url is None:
                    url = credentials.get("url", "https://api.freedomrobotics.ai/")
                self.token = credentials.get("token")
                self.secret = credentials.get("secret")
                api_auth(self.token, self.secret, url=url)
        else:
            raise Exception("Required: either token/secret, username/password, or saved ~/.freedom_credentials file")

    def get_account(self, account_id):
        """:obj:`Account`: Fetch an account by its account ID (Axxxxxxxxxxxx).

        Args:
            account_id (str): Account ID.
        """

        account_data = api_call("GET", "/accounts/{}".format(account_id))
        if not account_data:
            return None
        return Account(account_data["account"], account_data)

    def get_accounts(self):
        """:obj:`list` of :obj:`Account`: Fetch a list of all accounts that are visible/accessible.
        """

        result = api_call("GET", "/accounts")
        if not result:
            return []
        return [Account(account_data["account"], account_data) for account_data in result]

    def get_users(self):
        """:obj:`list` of :obj:`User`: Fetch a list of all users that are visible/accessible.
        """

        result = api_call("GET", "/users")
        if not result:
            return []
        return [User(user_data["user"], user_data) for user_data in result]

    def get_tokens(self):
        """:obj:`list` of :obj:`dict`: Fetch a list of tokens.
        """

        result = api_call("GET", "/accounts")
        return result

    def report_issue(self, message, level, logs=None, account=None, device=None, user=None, **kwargs):
        """Reports an issue to the API

        Args:
            message (str): The string with the error message.
            level (str): One of info, warning, error or fatal.
            logs (list of str): List of logs describing the issue.
            account (str): The account id if present.
            device (str): The device id if present.
            user (str): The user if prsent.
            **kwargs (dict): All the extra arguments will be sent into the body.
        """
        
        if level not in ('fatal', 'warning', 'error', 'info'):
            raise Exception(
                "Invalid level {}. Must be one of fatal, warning or error".format(level)
            )

        freedom_data = {
            "token": '*' * 3 + self.token[-8:],
        }
        if account is not None:
            freedom_data['account'] = account
        if device is not None:
            freedom_data['device'] = device
        if user is not None:
            freedom_data['user'] = user

        system_data = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "environment": os.environ.copy(),
        }
        if logs is None:
            logs = []

        exc_info = sys.exc_info()
        if any(exc_info):
            logs.extend(traceback.format_exception(**exc_info))

        data = {
            "message": message,
            "level": level,
            "logs": logs,
            "component": "api_client",
            "attributes": {
                "freedom_robotics": freedom_data,
                "python": {
                    "build": platform.python_build(),
                    "implementation": platform.python_implementation(),
                    "version": platform.python_version(),
                },
                "freedomrobotics_api_client": {
                    "version": __version__,
                    "install_path": os.path.abspath(os.path.dirname(__file__)),
                },
                "system": system_data,     
                "thread": {
                    "name": threading.current_thread().name,
                    "daemon": threading.current_thread().daemon
                }
            }
        }
        data.update(kwargs)

        api_call("PUT", "/issues", data=data)
