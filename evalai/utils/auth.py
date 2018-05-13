import json
from pathlib import Path

from click import echo


CONFIG_FILE = 'token.json'
FULL_PATH = str(Path.home()) + "/.evalai/{}".format(CONFIG_FILE)


def load_token():
    """
    Loads token to be used for sending requests.
    """
    with open(FULL_PATH, 'r') as fr:
        try:
            data = fr.read()
        except (OSError, IOError) as e:
            echo(e)
    data = json.loads(data)
    token = data["token"]
    return token
