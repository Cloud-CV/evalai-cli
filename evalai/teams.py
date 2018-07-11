import click

from evalai.utils.teams import (
                                create_team,
                                display_teams,
                               )


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--host', '-h', is_flag=True,
              help="View your host teams.")
def teams(ctx, host):
    """
    List all the participant/host teams of a user.

    Invoked by running `evalai teams`
    """
    if ctx.invoked_subcommand is None:
        display_teams(host)


@teams.command()
@click.option('--host', '-h', is_flag=True,
              help="Create a host team.")
def create(host):
    """
    Create a participant or host team.

    Invoked by running `evalai teams create`
    """
    team_name = click.prompt("Enter team name: ", type=str)
    if click.confirm("Please confirm the team name - %s" % (team_name), abort=True):
        create_team(team_name, host)
