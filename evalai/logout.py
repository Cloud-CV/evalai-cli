import click

from click import echo, style

from evalai.utils.auth import reset_user_auth_token


@click.group(invoke_without_command=True)
def logout():
    """
    Log out the user by resetting authentication token
    """
    """
    Invoked by `evalai logout`
    """
    reset_user_auth_token()
    echo(style("Logout successful", bold=True, fg="green"))
