import click

from click import echo, style

from .login import login
from .main import main
from .set_host import host as set_host  # 'host' would be a confusing name
from evalai.utils.auth import (
    get_host_url,
    get_user_auth_token,
    get_user_auth_token_by_login
)

previous_host_url = get_host_url()
username_help_message = "Required: Your EvalAI username"
password_help_message = "Required: Your EvalAI password"
host_help_message = "Optional: URL of the API host,\
                    currently set to: {}".format(previous_host_url)


@click.command
@click.option('-h', '--host',
              default=previous_host_url,
              help=host_help_message)
@click.option('-p', '--password', prompt=True, help=password_help_message)
@click.option('-u', '--username', prompt=True, help=username_help_message)
@click.pass_context
def ignite(ctx, username, password, host):
    """
    Set up basic configuration: host and auth key
    """
    """
    Invoked by `evalai ignite -u USER -p PASSWORD [-h HOST]`
    """
    echo(style("Booting up EvalAI", bold=True))
    ctx.invoke(main)
    if host != previous_host_url:
        ctx.invoke(set_host, set_host=host)
    if get_host_url() == host:  # check if the set_host command worked.
        ctx.invoke(login, username=username, password=password)
        current_auth_token = get_user_auth_token()
        user_auth_token = get_user_auth_token_by_login(username, password)
        if current_auth_token != user_auth_token:
            echo(style("Login failed.", bold=True))
            if host != previous_host_url:
                message = "Reverting host URL from {0} to {1}"
                echo(style(message.format(host, previous_host_url), bold=True))
                ctx.invoke(set_host, set_host=previous_host_url)
            sys.exit(1)
        else:
            echo(style("Setup successful."))
            sys.exit(0)
    else:
        # A more detailed error message is shown by set_host command already.
        echo(style("Couldn't set host URL to {}".format(host), bold=True))
        # Using get_host_url() rather than previous_host_url so that any
        # future bugs are discovered easily.
        echo(style("Current host URL: {}".format(get_host_url()), bold=True))
        sys.exit(1)
