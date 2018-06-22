import requests
import sys

from bs4 import BeautifulSoup
from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.common import validate_token
from evalai.utils.urls import URLS
from evalai.utils.config import API_HOST_URL, EVALAI_ERROR_CODES


def pretty_print_challenge_data(challenge):
    """
    Function to print the challenge data
    """
    br = style("----------------------------------------"
               "--------------------------", bold=True)

    challenge_title = "\n{}".format(style(challenge["title"],
                                    bold=True, fg="green"))
    challenge_id = "ID: {}\n\n".format(style(str(challenge["id"]),
                                       bold=True, fg="blue"))

    title = "{} {}".format(challenge_title, challenge_id)

    cleaned_desc = BeautifulSoup(challenge["short_description"], "lxml").text
    description = "{}\n".format(cleaned_desc)
    date = "End Date : {}".format(style(challenge["end_date"].split("T")[0], fg="red"))
    date = "\n{}\n\n".format(style(date, bold=True))
    challenge = "{}{}{}{}".format(title, description, date, br)
    echo(challenge)


def display_challenges(url):
    """
    Function to fetch & display the challenge list based on API
    """

    header = get_request_header()
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()
    if validate_token(response):

        challenges = response["results"]
        if len(challenges) is not 0:
            for challenge in challenges:
                pretty_print_challenge_data(challenge)
        else:
            echo("Sorry, no challenges found!")


def display_all_challenge_list():
    """
    Displays the list of all challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
    display_challenges(url)


def display_past_challenge_list():
    """
    Displays the list of past challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.past_challenge_list.value)
    display_challenges(url)


def display_ongoing_challenge_list():
    """
    Displays the list of ongoing challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
    display_challenges(url)


def display_future_challenge_list():
    """
    Displays the list of future challenges from the backend
    """
    url = "{}{}".format(API_HOST_URL, URLS.future_challenge_list.value)
    display_challenges(url)


def get_participant_or_host_teams(url):
    """
    Returns the participant or host teams corresponding to the user
    """
    header = get_request_header()

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response = response.json()

    if validate_token(response):
        return response['results']
    else:
        echo("The authentication token is not valid. Please try again!")
        sys.exit(1)


def get_participant_or_host_team_challenges(url, teams):
    """
    Returns the challenges corresponding to the participant or host teams
    """
    challenges = []
    for team in teams:
        header = get_request_header()
        try:
            response = requests.get(url.format(team['id']), headers=header)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            echo(err)
            sys.exit(1)
        response = response.json()
        challenges += response['results']
    return challenges


def display_participated_or_hosted_challenges(is_host=False, is_participant=False):
    """
    Function to display the participated or hosted challenges by a user
    """

    challenges = []

    if is_host:
        team_url = "{}{}".format(API_HOST_URL,
                                 URLS.host_teams.value)
        challenge_url = "{}{}".format(API_HOST_URL,
                                      URLS.host_challenges.value)

        teams = get_participant_or_host_teams(team_url)
        challenges = get_participant_or_host_team_challenges(challenge_url, teams)
        echo(style("\nHosted Challenges\n", bold=True))

        if len(challenges) != 0:
            for challenge in challenges:
                pretty_print_challenge_data(challenge)
        else:
            echo("Sorry, no challenges found!")

    if is_participant:
        team_url = "{}{}".format(API_HOST_URL,
                                 URLS.participant_teams.value)
        challenge_url = "{}{}".format(API_HOST_URL,
                                      URLS.participant_challenges.value)

        teams = get_participant_or_host_teams(team_url)
        challenges = get_participant_or_host_team_challenges(challenge_url, teams)
        echo(style("\nParticipated Challenges\n", bold=True))

        if len(challenges) != 0:
            for challenge in challenges:
                pretty_print_challenge_data(challenge)
        else:
            echo("Sorry, no challenges found!")


def pretty_print_challenge_phases(phases):
    """
    Function to print all the challenge phase of a challenge.
    """
    for phase in phases:
        br = style("--------------------------------"
                   "----------------------------------", bold=True)

        phase_title = "\n{}".format(style(phase["name"], bold=True,
                                          fg="green"))
        challenge_id = "Challenge ID: {}".format(style(str(phase["challenge"]),
                                                       bold=True, fg="blue"))
        phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]),
                                                   bold=True, fg="blue"))

        title = "{} {} {}".format(phase_title, challenge_id, phase_id)

        cleaned_desc = BeautifulSoup(phase["description"], "lxml").text
        description = "{}\n\n".format(cleaned_desc)
        phase = "{}{}{}".format(title, description, br)
        echo(phase)


def display_challenge_phase_list(challenge_id):
    """
    Function to display all challenge phases for a particular challenge.
    """
    url = URLS.challenge_phase_list.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id)
    headers = get_request_header()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            echo(style("Error: " + response.json()["error"], fg="red", bold=True))
        else:
            echo(err)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()
    if validate_token(response_json):
        phases = response_json["results"]
        pretty_print_challenge_phases(phases)


def pretty_print_challenge_phase(phase):
    """
    Function to print the details of a challenge phase.
    """
    phase_title = "\n{}".format(style(phase["name"], bold=True, fg="green"))
    challenge_id = "Challenge ID: {}".format(style(str(phase["challenge"]), bold=True, fg="blue"))
    phase_id = "Phase ID: {}\n\n".format(style(str(phase["id"]), bold=True, fg="blue"))

    title = "{} {} {}".format(phase_title, challenge_id, phase_id)

    cleaned_desc = BeautifulSoup(phase["description"], "lxml").text
    description = "{}\n".format(cleaned_desc)

    start_date = "Start Date : {}".format(style(phase["start_date"].split("T")[0], fg="green"))
    start_date = "\n{}\n".format(style(start_date, bold=True))

    end_date = "End Date : {}".format(style(phase["end_date"].split("T")[0], fg="red"))
    end_date = "\n{}\n".format(style(end_date, bold=True))
    max_submissions_per_day = style("\nMaximum Submissions per day : {}\n".format(
                                    str(phase["max_submissions_per_day"])), bold=True)

    max_submissions = style("\nMaximum Submissions : {}\n".format(str(phase["max_submissions"])),
                            bold=True)

    codename = style("\nCode Name : {}\n".format(phase["codename"]), bold=True)
    leaderboard_public = style("\nLeaderboard Public : {}\n".format(phase["leaderboard_public"]), bold=True)
    is_active = style("\nActive : {}\n".format(phase["is_active"]), bold=True)
    is_public = style("\nPublic : {}\n".format(phase["is_public"]), bold=True)

    phase = "{}{}{}{}{}{}{}{}{}{}".format(title, description, start_date,
                                          end_date,
                                          max_submissions_per_day,
                                          max_submissions,
                                          leaderboard_public,
                                          codename, is_active, is_public)
    echo(phase)


def display_challenge_phase_detail(challenge_id, phase_id):
    """
    Function to print details of a challenge phase.
    """
    url = URLS.challenge_phase_detail.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id, phase_id)
    headers = get_request_header()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            echo(style("Error: " + response.json()["error"], fg="red", bold=True))
        else:
            echo(err)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()

    if validate_token(response_json):
        phase = response_json
        pretty_print_challenge_phase(phase)
