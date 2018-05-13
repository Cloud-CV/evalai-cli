import click

from click import echo


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
        echo('Hello all!')


@click.command(name='ongoing')
def list_ongoing_challenges():
    """
    Lists currently active challenges.
    """
    echo('Hello currently active!')


@click.command(name='past')
def list_past_challenges():
    """
    Lists past challenges.
    """
    echo('Hello past!')


@click.command(name='future')
def list_future_challenges():
    """
    Lists future challenges.
    """
    echo('Hello future!')


# Command -> evalai challenges list
challenges.add_command(list_challenges)

# Command -> evalai challenges list ongoing/past/future
list_challenges.add_command(list_ongoing_challenges)
list_challenges.add_command(list_past_challenges)
list_challenges.add_command(list_future_challenges)
