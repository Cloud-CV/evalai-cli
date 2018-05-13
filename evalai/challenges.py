import click

from click import echo

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,)


@click.group(invoke_without_command=True)
@click.pass_context
def challenges(ctx):
    """
    Challenges and related Options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = """Welcome to the EvalAI CLI. Use evalai challenges --help for viewing all the options"""
        echo(welcome_text)


@click.group(invoke_without_command=True, name='list')
@click.pass_context
def list_challenges(ctx):
    """
    Lists all challenges.
    """
    if ctx.invoked_subcommand is None:
        get_challenge_list()


@click.command(name='past')
def list_past_challenges():
    """
    Lists past challenges.
    """
    get_past_challenge_list()


@click.command(name='future')
def list_future_challenges():
    """
    Lists future challenges.
    """
    get_future_challenge_list()


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)
