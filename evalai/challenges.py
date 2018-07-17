import click

from click import style

from evalai.utils.common import Date
from evalai.utils.challenges import (
    display_all_challenge_list,
    display_future_challenge_list,
    display_ongoing_challenge_list,
    display_past_challenge_list,
    display_participated_or_hosted_challenges,
    display_challenge_details,
    display_challenge_phase_list,
    display_challenge_phase_detail,
    display_challenge_phase_split_list,
    display_leaderboard,
)
from evalai.utils.submissions import display_my_submission_details
from evalai.utils.teams import participate_in_a_challenge
from evalai.utils.submissions import make_submission


class Challenge(object):
    """
    Stores user input ID's
    """

    def __init__(self, challenge=None, phase=None, subcommand=None):
        """
        Args
        ----------
        challenge: Int
            Challenge ID to be stored
        phase: Int
            Phase ID to be stored
        subcommand: string
            Subcommand to be stored
        """
        self.challenge_id = challenge
        self.phase_id = phase
        self.subcommand = subcommand


class PhaseGroup(click.Group):
    """
    Fetch the submcommand data in the phase group
    """

    def invoke(self, ctx):
        """
        Parses Subcommands to be stored in Challenge Object

        Args
        ----------
        ctx: Context Object
        """
        if "--json" in tuple(ctx.protected_args):
            ctx.protected_args = []
            ctx.params["json"] = True
        subcommand = tuple(ctx.protected_args)
        ctx.obj.subcommand = subcommand
        super(PhaseGroup, self).invoke(ctx)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--participant",
    is_flag=True,
    help="List the challenges that you've participated",
)
@click.option(
    "--host", is_flag=True, help="List the challenges that you've hosted"
)
def challenges(ctx, participant, host):
    """
    Lists challenges
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    participant (optional flag): Bool
        Returns participated challenges

    host (optional flag): Bool
        Returns hosted challenges

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular challenges

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenges
    """
    if participant or host:
        display_participated_or_hosted_challenges(host, participant)
    elif ctx.invoked_subcommand is None:
        display_all_challenge_list()


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument("CHALLENGE", type=int)
def challenge(ctx, challenge):
    """
    Display challenge specific details
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    CHALLENGE (Argument): Int
        Challenge ID

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular challenge details

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenge CHALLENGE <OPTIONAL COMMANDS>
    """
    ctx.obj = Challenge(challenge=challenge)
    if ctx.invoked_subcommand is None:
        display_challenge_details(challenge)


@challenges.command()
def ongoing():
    """
    List all active challenges
    """
    """
    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular ongoing challenges

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenge ongoing
    """
    display_ongoing_challenge_list()


@challenges.command()
def past():
    """
    List all past challenges
    """
    """
    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular past challenges.

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge past
    """
    display_past_challenge_list()


@challenges.command()
def future():
    """
    List all upcoming challenges
    """
    """
    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular upcoming challenges

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge future
    """
    display_future_challenge_list()


@challenge.command()
@click.pass_obj
def phases(ctx):
    """
    List all phases of a challenge
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular phases

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge CHALLENGE phases
    """
    display_challenge_phase_list(ctx.challenge_id)


@click.group(invoke_without_command=True, cls=PhaseGroup)
@click.pass_obj
@click.option("--json", is_flag=True, help="Get phase details in JSON format.")
@click.argument("PHASE", type=int)
def phase(ctx, json, phase):
    """
    List phase details of a phase
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    json (optional flag): Bool
        Returns phase details as json

    PHASE (Argument): Int
        PHASE ID

    Returns
    -------
    Phase Description: String
        Phase Description

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge CHALLENGE phase PHASE <OPTIONAL COMMANDS>
    """
    ctx.phase_id = phase
    if len(ctx.subcommand) == 0:
        display_challenge_phase_detail(ctx.challenge_id, phase, json)


@phase.command()
@click.pass_obj
@click.option(
    "--start-date",
    "-s",
    type=Date(format="%m/%d/%y"),
    help="Start date for submissions in `mm/dd/yyyy` format.",
)
@click.option(
    "--end-date",
    "-e",
    type=Date(format="%m/%d/%y"),
    help="End date for submissions in `mm/dd/yyyy` format.",
)
def submissions(ctx, start_date, end_date):
    """
    Display submissions to a particular challenge
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular submissions to a challenge

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenge CHALLENGE phase PHASE submissions
    """
    display_my_submission_details(
        ctx.challenge_id, ctx.phase_id, start_date, end_date
    )


@phase.command()
@click.pass_obj
def splits(ctx):
    """
    View the phase splits of a challenge
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular phase splits of a phase

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenge CHALLENGE phase PHASE splits
    """
    display_challenge_phase_split_list(ctx.challenge_id)


@challenge.command()
@click.pass_obj
@click.argument("CPS", type=int)
def leaderboard(ctx, cps):
    """
    Displays the Leaderboard to a Challenge Phase Split
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    CPS (Argument): Int
        Challenge Phase Split ID

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular leaderboard of the Challenge Phase Split

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    ValueError
        Invalid Date Format

    Command
    -------
    evalai challenge CHALLENGE leaderboard CPS
    """
    display_leaderboard(ctx.challenge_id, cps)


@challenge.command()
@click.pass_obj
@click.argument("TEAM", type=int)
def participate(ctx, team):
    """
    Participate in a challenge
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    TEAM (Argument): Int
        Team ID

    Returns
    -------
    String
       Participation status

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge CHALLENGE participate TEAM
    """
    participate_in_a_challenge(ctx.challenge_id, team)


@phase.command()
@click.pass_obj
@click.option(
    "--file", type=click.File("rb"), help="File path to the submission file"
)
def submit(ctx, file):
    """
    Make submission to a challenge
    """
    """
    Args
    ----------
    ctx: Context Object
        Click Context Object

    file (required flag): click.File
        File for submission

    Returns
    -------
    String
       File submission status

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception

    Command
    -------
    evalai challenge CHALLENGE participate PHASE submit --file FILE
    """
    submission_metadata = {}
    if click.confirm("Do you want to include the Submission Details?"):
        submission_metadata["method_name"] = click.prompt(
            style("Method Name", fg="yellow"), type=str, default=""
        )
        submission_metadata["method_description"] = click.prompt(
            style("Method Description", fg="yellow"), type=str, default=""
        )
        submission_metadata["project_url"] = click.prompt(
            style("Project URL", fg="yellow"), type=str, default=""
        )
        submission_metadata["publication_url"] = click.prompt(
            style("Publication URL", fg="yellow"), type=str, default=""
        )
    make_submission(ctx.challenge_id, ctx.phase_id, file, submission_metadata)


challenge.add_command(phase)
