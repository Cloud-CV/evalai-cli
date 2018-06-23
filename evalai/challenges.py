import click

from evalai.utils.challenges import (
                                    display_all_challenge_list,
                                    display_future_challenge_list,
                                    display_ongoing_challenge_list,
                                    display_past_challenge_list,
                                    display_participated_or_hosted_challenges,
                                    display_challenge_phase_list,
                                    display_challenge_phase_detail,)


class Challenge(object):
    def __init__(self, challenge=None, phase=None):
        self.challenge_id = challenge
        self.phase_id = phase


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--participant', is_flag=True,
              help="List the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="List the challenges that you've hosted")
def challenges(ctx, participant, host):
    """
    Lists challenges

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
    Displays challenge specific details.
    """
    ctx.obj = Challenge(challenge)


@challenges.command()
def ongoing():
    """
    List all active challenges

    Invoked by running `evalai challenges ongoing`
    """
    display_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges

    Invoked by running `evalai challenges past`
    """
    display_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges

    Invoked by running `evalai challenges future`
    """
    display_future_challenge_list()


@challenge.command()
@click.pass_obj
def phases(ctx):
    """
    List all phases of a challenge

    Invoked by running `evalai challenges CHALLENGE phases`
    """
    display_challenge_phase_list(ctx.challenge_id)


@challenge.command()
@click.pass_obj
@click.argument('PHASE', type=int)
def phase(ctx, phase):
    """
    List phase details of a phase

    Invoked by running `evalai challenges CHALLENGE phase PHASE`
    """
    display_challenge_phase_detail(ctx.challenge_id, phase)
