import click
import validators

from click import echo, style

from evalai.utils.auth import write_auth_token_to_file
from evalai.utils.config import LEN_OF_TOKEN


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
        write_auth_token_to_file(auth_token)
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
                fg="red"
            )
        )
