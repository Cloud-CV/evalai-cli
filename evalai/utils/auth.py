import json
from pathlib import Path

from click import echo


CONFIG_FILE = 'token.json'
AUTH_TOKEN_PATH = "{}/.evalai/{}".format(str(Path.home()), CONFIG_FILE)


def get_token():
    """
    Loads token to be used for sending requests.
    """
    with open(AUTH_TOKEN_PATH, 'r') as TokenObj:
        try:
            data = TokenObj.read()
        except (OSError, IOError) as e:
            echo(e)
    data = json.loads(data)
    token = data["token"]
    return token


def get_headers():
    """
    Returns token formatted in header for sending requests.
    """
    headers = {
            "Authorization": "Token {}".format(get_token()),
    }

    return headers
