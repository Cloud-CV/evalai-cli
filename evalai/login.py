import os
import click

from click import echo, style
from evalai.utils.auth import get_user_auth_token_by_login
from evalai.utils.common import store_data_to_json
from evalai.utils.config import AUTH_TOKEN_PATH, AUTH_TOKEN_DIR


@click.group(invoke_without_command=True)
@click.pass_context
def login(ctx):
    """
    Login to EvalAI and save token.
    """
    username = click.prompt("username", type=str, hide_input=False)
    password = click.prompt("Enter password", type=str, hide_input=True)
    token = get_user_auth_token_by_login(username, password)

    if not os.path.exists(AUTH_TOKEN_DIR):
        os.makedirs(AUTH_TOKEN_DIR)
    store_data_to_json(AUTH_TOKEN_PATH, token, "Unable to store token data due to error: {}")

    echo(style("\nLogged in successfully!", bold=True))
