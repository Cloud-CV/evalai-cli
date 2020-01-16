import click
import os

from click import echo, style

from evalai.utils.auth import get_user_auth_token
from evalai.utils.config import AUTH_TOKEN_PATH
import json


@click.group(invoke_without_command=True)
def get_token():
    """
    Get the EvalAI token.
    """
    if not os.path.exists(AUTH_TOKEN_PATH):
        echo(
            style(
                "\nThe authentication token json file doesn't exists at the required path. "
                "Please download the file from the Profile section of the EvalAI webapp and "
                "place it at ~/.evalai/token.json or use evalai set_token <token> to add it.\n",
                bold=True,
                fg="red",
            )
        )
        sys.exit(1)
    else:
        token = get_user_auth_token()
        echo(f"Current token is {token}")
