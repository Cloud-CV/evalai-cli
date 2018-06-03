import click

from click import echo

from evalai.utils.teams import (
                                get_participant_teams,
                                create_participant_team,
                                challenge_participate
                               )


@click.group(invoke_without_command=True)
@click.pass_context
def teams(ctx):
    """
    Teams and related options.
    """
    if ctx.invoked_subcommand is None:
        welcome_text = ("Welcome to the EvalAI CLI."
                        "Use `evalai teams --help` for viewing all the options.")
        echo(welcome_text)


@click.command(name='list')
def list_teams():
    """
    Used to list all the participant teams of a user.
    Invoked by running `evalai teams list`
    """
    get_participant_teams()


@click.command(name='create')
def create_team():
    """
    Used to create participant team.
    Invoked by running `evalai teams create`
    """
    team_name = click.prompt("Enter team name: ", type=str)
    if click.confirm("Please confirm the team name - %s" % (team_name), abort=True):
        create_participant_team(team_name)


@click.command(name='participate')
@click.option('-c', '--challenge-id', type=int,
              help="Challenge ID for participating.",
              required=True)
@click.option('-pt', '--participant-team', type=int,
              help="Challenge ID for participating.",
              required=True)
def participate(challenge_id, participant_team):
    """
    Used to create participant team.
    Invoked by running `evalai teams participate`
    """
    challenge_participate(challenge_id, participant_team)


# Command -> evalai challenges list
teams.add_command(list_teams)

# Command -> evalai challenges create
teams.add_command(create_team)

# Command -> evalai challenges participate
teams.add_command(participate)
