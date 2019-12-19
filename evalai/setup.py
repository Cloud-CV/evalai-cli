import click
import sys

from click import echo, style

from evalai.utils.auth import (
    get_host_url,
    get_user_auth_token_by_login,
    validate_and_write_host_url_to_file,
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
@click.option('-h', '--host',
              default=None,
              help=host_help_message)
@click.option('-p', '--password', prompt=True, help=password_help_message)
@click.option('-u', '--username', prompt=True, help=username_help_message)
def ignite(username, password, host):
    """
    Set up basic configuration: host and auth key
    """
    """
    Invoked by `evalai ignite` or `evalai ignite -u USER -p PASSWORD [-h HOST]`
    """
    echo(style("Booting up EvalAI", bold=True))
    echo(welcome_text)
    if host:
        previous_host = get_host_url()  # In case reverting is required
        validate_and_write_host_url_to_file(host)
    try:
        token = get_user_auth_token_by_login(username, password)
        write_json_auth_token_to_file(token)
        echo(style("\nLogged in successfully!"))
    except Exception as e:
        echo(style("\nLogin failed.", bold=True))
        if host:
            echo(style("Reverting host URL from {} to {}".format(host, previous_host), bold=True))
            validate_and_write_host_url_to_file(previous_host)
        echo(e)
    echo(style("\nSetup successful!", bold=True, fg="green"))
