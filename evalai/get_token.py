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
    token = get_user_auth_token()
    echo(f"Current token is {token}")
