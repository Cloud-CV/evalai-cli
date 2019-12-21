import click
import sys
import validators

from click import echo, style

from evalai.utils.auth import (
    get_host_url,
    get_user_auth_token_by_login,
    write_host_url_to_file,
    write_json_auth_token_to_file,
)

previous_host_url = get_host_url()
username_help_message = "Required: Your EvalAI username"
password_help_message = "Required: Your EvalAI password"
host_help_message = "Optional: URL of the API host,\
                    currently set to: {}".format(previous_host_url)
welcome_text = (
    """
                #######                  ###      ###    #######
                ##      ##   ##   #####  ###     #####     ###
                #####    ## ##   ##  ##  ###    ##   ##    ###
                ##        ###   ###  ##  #####  #######    ###
                #######    #     ### ### #####  ##   ##  #######\n\n"""
    "Welcome to the EvalAI CLI. Use evalai --help for viewing all the options\n"
    "CHALLENGE and PHASE placeholders used throughout the CLI are"
    " for challenge_id\nand phase_id of the challenges and phases."
)


@click.group(invoke_without_command=True)
@click.option('-u', '--username', type=str, prompt=True,
              hide_input=False, help=username_help_message)
@click.option('-p', '--password', type=str, prompt=True,
              hide_input=True, help=password_help_message)
@click.option('-h', '--host', type=str, default='', help=host_help_message)
def setup(host, password, username):
    """
    Set up basic configuration: host and auth key
    """
    """
    Invoked by `evalai setup` or `evalai setup -u USER -p PASSWORD [-h HOST]`
    """
    echo(style("Booting up EvalAI", bold=True))
    echo(style(welcome_text, bold=True))
    if host:
        if not validators.url(host):
            echo(
                style(
                    "Sorry, please enter a valid url.\n"
                    "Example: https://evalapi.cloudcv.org",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        # In case reverting is required
        previous_host = get_host_url()
        try:
            write_host_url_to_file(host)
        except SystemExit as e:
            echo(
                style(
                    "Couldn't set host URL to {}\nCurrent host URL: {}".format(host, previous_host),
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
    try:
        token = get_user_auth_token_by_login(username, password)
        write_json_auth_token_to_file(token)
        echo(style("\nLogged in successfully!"))
    except (SystemExit, Exception) as e:  # Accommodating sys.exit!
        echo(style("\nLogin failed.", bold=True, fg="red"))
        if host != previous_host:
            echo(style("Reverting host URL from {} to {}".format(host, previous_host), bold=True))
            write_host_url_to_file(previous_host)  # Validation not required while restoring
        echo(e)
        sys.exit(1)
    echo(style("\nSetup successful!", bold=True, fg="green"))
