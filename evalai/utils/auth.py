import os
import requests

from click import echo


CONFIG_FILE = '.config'
__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                    os.path.dirname(__file__)))
FULL_PATH = os.path.join(__location__, CONFIG_FILE)


def save_token(token):
    """
    Saves the token in a config file.
    """
    with open(FULL_PATH, 'w') as fw:
        try:
            fw.write(token)
            echo('Your token has been saved.')
        except (OSError, IOError) as e:
            echo(e)


def load_token():
    """
    Loads token to be used for sending requests.
    """
    token = ''
    with open(FULL_PATH, 'r') as fr:
        try:
            token = fr.read()
        except (OSError, IOError) as e:
            echo(e)
    return token
