import click
import sys

from click import echo, style

from .challenges import challenge, challenges
from .set_host import host
from .add_token import set_token
from .submissions import submission, push, download_file
from .teams import teams
from .get_token import get_token
from .login import login
from .utils.updates import get_latest_version
from .version import __version__


@click.version_option()
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """
    Welcome to the EvalAI CLI.
    """
    if ctx.invoked_subcommand is None:
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
        echo(welcome_text)
    latest_version = get_latest_version()
    if __version__ < latest_version:
        echo(
            style(
                "\nUpdate:\n"
                "\nPlease install the latest version of EvalAI-CLI!\n",
                "\nUse: pip install --upgrade evalai\n",
                fg="red",
                bold=True,
            )
        )
        sys.exit(1)


main.add_command(challenges)
main.add_command(challenge)
main.add_command(download_file)
main.add_command(host)
main.add_command(push)
main.add_command(set_token)
main.add_command(submission)
main.add_command(teams)
main.add_command(get_token)
main.add_command(login)
