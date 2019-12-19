import click

from click import echo, style
from evalai.utils.auth import get_user_auth_token_by_login, write_json_auth_token_to_file


@click.group(invoke_without_command=True)
@click.option('-p', '--password', type=str, hide_input=True, prompt=True)
@click.option('-u', '--username', type=str, hide_input=False, prompt=True)
@click.pass_context
def login(ctx, username, password):
    """
    Login to EvalAI and save token.
    """
    token = get_user_auth_token_by_login(username, password)
    write_json_auth_token_to_file(token)
    echo(style("\nLogged in successfully!", bold=True))
