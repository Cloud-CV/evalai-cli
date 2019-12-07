import os

import click
import json
import validators

from click import echo, style

from evalai.utils.config import AUTH_TOKEN_DIR, AUTH_TOKEN_PATH, LEN_OF_TOKEN
from evalai.utils.auth import get_user_auth_token_by_login


@click.group(invoke_without_command=True)
@click.argument("auth_token")
def set_token(auth_token):
    """
    Configure EvalAI Token.
    """
    """
    Invoked by `evalai set_token <your_evalai_auth_token>`.
    """
    if validators.length(auth_token, min=LEN_OF_TOKEN, max=LEN_OF_TOKEN):
        if not os.path.exists(AUTH_TOKEN_DIR):
            os.makedirs(AUTH_TOKEN_DIR)
        username = click.prompt("Enter username", type=str, hide_input=False)
        password = click.prompt("Enter password", type=str, hide_input=True)
        token_from_server = get_user_auth_token_by_login(username, password)["token"]
        with open(AUTH_TOKEN_PATH, "w+") as fw:
            if auth_token != token_from_server:
                echo(
                    style(
                        "Error: Token invalid. Entered token and token from server doesn't match.",
                        bold=True,
                        fg="red",
                    )
                )
            else:
                try:
                    auth_token = {"token": "{}".format(auth_token)}  # noqa
                    auth_token = json.dumps(auth_token)
                    fw.write(auth_token)
                except (OSError, IOError) as e:
                    echo(e)
                echo(
                    style(
                        "Success: Authentication token is successfully set.",
                        bold=True,
                        fg="green",
                    )
                )
    else:
        echo(
            style(
                "Error: Invalid Length. Enter a valid token of length: {}".format(
                    LEN_OF_TOKEN
                ),
                bold=True,
            )
        )
