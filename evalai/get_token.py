import click

from click import echo

from evalai.utils.auth import get_user_auth_token


@click.group(invoke_without_command=True)
def get_token():
    """
    Get the EvalAI token.
    """
    token = get_user_auth_token()
    echo("Current token is {0}".format(token))
