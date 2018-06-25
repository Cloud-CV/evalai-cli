import click

from evalai.utils.challenges import (
                                    display_all_challenge_list,
                                    display_future_challenge_list,
                                    display_ongoing_challenge_list,
                                    display_past_challenge_list,
                                    display_participated_or_hosted_challenges,)
from evalai.utils.teams import participate_in_a_challenge
from evalai.utils.submissions import submit_a_file


class Challenge(object):
    """
    Stores user input ID's.
    """
    def __init__(self, challenge_id=None, phase_id=None):
        self.challenge_id = challenge_id
        self.phase_id = phase_id


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--participant', is_flag=True,
              help="List the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="List the challenges that you've hosted")
def challenges(ctx, participant, host):
    """
    Lists challenges
    """
    """
    Invoked by running `evalai challenges`
    """
    if participant or host:
        display_participated_or_hosted_challenges(host, participant)
    elif ctx.invoked_subcommand is None:
        display_all_challenge_list()


@click.group()
@click.pass_context
@click.argument('CHALLENGE', type=int)
def challenge(ctx, challenge):
    """
    View challenge specific details.
    """
    ctx.obj = Challenge(challenge_id=challenge)


@challenges.command()
def ongoing():
    """
    List all active challenges
    """
    """
    Invoked by running `evalai challenges ongoing`
    """
    display_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges
    """
    """
    Invoked by running `evalai challenges past`
    """
    display_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges
    """
    """
    Invoked by running `evalai challenges future`
    """
    display_future_challenge_list()


@challenge.command()
@click.pass_obj
@click.argument('TEAM', type=int)
def participate(ctx, team):
    """
    Participate in a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE participate TEAM`
    """
    participate_in_a_challenge(ctx.challenge_id, team)


@click.group(invoke_without_command=True)
@click.pass_obj
@click.argument('PHASE', type=int)
def phase(ctx, phase):
    """
    Displays phases as a list.
    Invoked by running `evalai challenge CHALLENGE phase PHASE`
    """
    ctx.phase_id = phase


@phase.command()
@click.pass_obj
@click.argument('FILE', type=click.File('rb'))
def submit(ctx, file):
    """
    Make submission to a challenge.
    """
    """
    Invoked by running `evalai challenge CHALLENGE phase PHASE submit FILE`
    """
    submit_a_file(ctx.challenge_id, ctx.phase_id, file)


challenge.add_command(phase)
