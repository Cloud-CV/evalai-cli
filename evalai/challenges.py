import click

from evalai.utils.challenges import (
                                    get_challenge_list,
                                    get_ongoing_challenge_list,
                                    get_past_challenge_list,
                                    get_future_challenge_list,
                                    get_participated_or_hosted_challenges,)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--participant', is_flag=True,
              help="List the challenges that you've participated")
@click.option('--host', is_flag=True,
              help="List the challenges that you've hosted")
def challenges(ctx, participant, host):
    """
    Lists challenges.
    Invoked by running `evalai challenges`
    """
    if participant or host:
        get_participated_or_hosted_challenges(host, participant)
    elif ctx.invoked_subcommand is None:
        get_challenge_list()


@challenges.command()
def ongoing():
    """
    List all active challenges.
    Invoked by running `evalai challenges ongoing`
    """
    get_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges.
    Invoked by running `evalai challenges past`
    """
    get_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges.
    Invoked by running `evalai challenges future`
    """
    get_future_challenge_list()
