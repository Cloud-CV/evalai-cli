import json
import requests
import sys

from beautifultable import BeautifulTable
from click import echo, style

from evalai.utils.auth import get_request_header, get_host_url
from evalai.utils.common import validate_token
from evalai.utils.urls import URLS
from evalai.utils.config import EVALAI_ERROR_CODES


requests.packages.urllib3.disable_warnings()


def pretty_print_team_data(teams, is_host):
    """
    Pretty print the team data

    Args
    ----------
    teams: dict
        Teams list as JSON

    Returns
    -------
    BeautifuleTable: BeautifulTable Object (string)
       Tabular teams
    """
    table = BeautifulTable(max_width=200)
    attributes = ["id", "team_name", "created_by"]
    columns_attributes = [
        "ID",
        "Team Name",
        "Created By",
        "Members",
        "Team URL",
    ]
    table.column_headers = columns_attributes
    for team in teams:
        values = list(map(lambda item: team[item], attributes))
        if is_host:
            members = ", ".join(
                map(lambda member: member["user"], team["members"])
            )
        else:
            members = ", ".join(
                map(lambda member: member["member_name"], team["members"])
            )
        values.append(members)
        if team["team_url"]:
            values.append(team["team_url"])
        else:
            values.append("None")
        table.append_row(values)
    echo(table)


def display_teams(is_host):
    """
    Fetch and display the participant or host teams of a user

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    """
    url = "{}{}"
    headers = get_request_header()
    if is_host:
        url = url.format(get_host_url(), URLS.host_team_list.value)
    else:
        url = url.format(get_host_url(), URLS.participant_team_list.value)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code in EVALAI_ERROR_CODES:
            validate_token(response.json())
            echo(
                style(
                    "Error: {}".format(response.json()["error"]),
                    fg="red",
                    bold=True,
                )
            )
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException:
        echo(
            style(
                "\nCould not establish a connection to EvalAI."
                " Please check the Host URL.\n",
                bold=True,
                fg="red",
            )
        )
        sys.exit(1)
    response = response.json()

    teams = response["results"]
    if len(teams) != 0:
        pretty_print_team_data(teams, is_host)
    else:
        echo("Sorry, no teams found.")


def create_team(team_name, team_url, is_host):
    """
    Create new participant or host team

    Args
    ----------
    team_name: String
        New team name

    Returns
    -------
    String: Team creation status

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    """
    url = "{}{}"

    if is_host:
        url = url.format(get_host_url(), URLS.create_host_team.value)
    else:
        url = url.format(get_host_url(), URLS.participant_team_list.value)

    headers = get_request_header()
    headers["Content-Type"] = "application/json"

    data = {}
    data["team_name"] = team_name
    if team_url:
        data["team_url"] = team_url
    data = json.dumps(data)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code in EVALAI_ERROR_CODES:
            validate_token(response.json())
            if "team_name" in response.json().keys():
                validate_token(response.json())
                echo(
                    style(
                        "Error: {}".format(response.json()["team_name"][0]),
                        fg="red",
                        bold=True,
                    )
                )
            else:
                echo(
                    style(
                        "Error: {}".format(response.json()["error"]),
                        fg="red",
                        bold=True,
                    )
                )
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException:
        echo(
            style(
                "\nCould not establish a connection to EvalAI."
                " Please check the Host URL.\n",
                bold=True,
                fg="red",
            )
        )
        sys.exit(1)

    if response.status_code == 201:
        response = response.json()
        if is_host:
            echo(
                style(
                    "\nYour host team {} was successfully created.\n".format(
                        response["team_name"]
                    ),
                    fg="green",
                    bold=True,
                )
            )
        else:
            echo(
                style(
                    "\nYour participant team {} was successfully created.\n".format(
                        response["team_name"]
                    ),
                    fg="green",
                    bold=True,
                )
            )


def participate_in_a_challenge(challenge_id, participant_team_id):
    """
    Request participation in a particular challenge

    Args
    ----------
    challenge_id: Int
        Challenge ID

    participant_team_id: Int
        Participant team ID

    Returns
    -------
    String: Participation status

    Raises
    -------
    requests.exceptions.HTTPError
        Server throws 4XX error
    requests.exceptions.RequestException
        Server throws request exception
    """
    url = "{}{}".format(get_host_url(), URLS.participate_in_a_challenge.value)
    url = url.format(challenge_id, participant_team_id)

    headers = get_request_header()
    headers["Content-Type"] = "application/json"
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code in EVALAI_ERROR_CODES:
            validate_token(response.json())
            echo(
                style(
                    "\nError: {}\n"
                    "\nUse `evalai challenges` to fetch the active challenges.\n"
                    "\nUse `evalai teams` to fetch your participant "
                    "teams.\n".format(response.json()["error"]),
                    fg="red",
                    bold=True,
                )
            )
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException:
        echo(
            style(
                "\nCould not establish a connection to EvalAI."
                " Please check the Host URL.\n",
                bold=True,
                fg="red",
            )
        )
        sys.exit(1)

    if response.status_code == 201:
        echo(
            style(
                "Your team id {} is now participating in this challenge.".format(
                    participant_team_id
                ),
                fg="green",
                bold=True,
            )
        )
