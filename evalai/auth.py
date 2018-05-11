import click

from click import echo

from evalai.utils.auth import save_token

@click.command()
@click.option('--token', '-t',
              default='',
              help='Pass token obtained from your EvalAI account.')
def auth(token):
    """
    Connect your EvalAI account with the CLI.
    """
    if (token == ''):
        echo("Please pass a Token. Use evalai auth --help for help.")
    else:
        save_token(token)
