import json
import os
import requests
import sys

from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.common import validate_token
from evalai.utils.urls import URLS


EVALAI_ERROR_CODES = [400, 401, 406]

API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def pretty_print_teams(teams):
    """
    Pretty prints the teams
    """
    for team in teams:
        br = style("----------------------------------------"
                   "--------------------------", bold=True)

        team_name = "\n{}".format(style(team["team_name"],
                                        bold=True, fg="green"))
        team_id = "ID: {}\n\n".format(style(str(team["id"]),
                                            bold=True, fg="blue"))
        title = "{} {}".format(team_name, team_id)
        created_by = "Created by : {}\n\n".format(style(team["created_by"], fg="blue"))
        members = "{}\n".format(style("Members", bold=True))
        for member in team["members"]:
            members = "{}* {}\n".format(members, member["member_name"])
        team = "{}{}{}\n{}".format(title, created_by, members, br)
        echo(team)


def display_participant_teams():
    """
    Function to fetch all the participant teams of a user.
    """
    headers = get_request_header()

    url = "{}{}".format(API_HOST_URL, URLS.participant_team_lists.value)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            echo(style("Error: " + response.json()["error"], fg="red", bold=True))
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)
    response_json = response.json()

    if validate_token(response_json):
        teams = response_json["results"]
        if len(teams) != 0:
            pretty_print_teams(teams)
        else:
            echo("Sorry, no teams found.")


def create_participant_team(team_name):
    """
    Function to create a new team by taking in the team name as input.
    """
    url = "{}{}".format(API_HOST_URL, URLS.participant_team_lists.value)

    headers = get_request_header()
    headers['Content-Type'] = 'application/json'

    data = {}
    data["team_name"] = team_name
    data = json.dumps(data)
    try:
        response = requests.post(
                                url,
                                headers=headers,
                                data=data
                                )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            if "team_name" in response.json().keys():
                echo(style("Error: {}".format(response.json()["team_name"][0]), fg="red", bold=True))
            else:
                echo(style("Error: " + response.json()['error'], fg="red", bold=True))
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()

    if response.status_code == 201:
        echo(style("\nThe team {} was successfully created.\n".format(response_json["team_name"]),
                   fg="green", bold=True))


def challenge_participate(challenge_id, participant_team_id):
    """
    Function to participate in a particular challenge.
    """

    url = "{}{}".format(API_HOST_URL, URLS.challenge_participate.value)
    url = url.format(challenge_id, participant_team_id)

    headers = get_request_header()
    headers['Content-Type'] = 'application/json'
    try:
        response = requests.post(
                                url,
                                headers=headers,
                                )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            echo(style("Error: " + response.json()["error"], fg="red", bold=True))
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    if response.status_code == 201:
        echo(style("Your participant team is now participating in this challenge.",
                   fg="green", bold=True))
