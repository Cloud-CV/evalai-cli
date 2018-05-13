import click

from click import echo


@click.command()
def auth():
    """Authentications and tokens."""
    echo('Hello auth!')
