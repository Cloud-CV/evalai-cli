import os
import requests
import sys

from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.urls import URLS
from evalai.utils.common import validate_token


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def submit_file(challenge_id, phase_id, file):

    """
    Function to create a new team by taking in the team name as input.
    """
    url = "{}{}".format(API_HOST_URL, URLS.submit_file.value)
    url = url.format(challenge_id, phase_id)

    headers = get_request_header()
    file = {'input_file': file}
    data = {
            'status': 'submitting',
           }

    try:
        response = requests.post(
                                url,
                                headers=headers,
                                files=file,
                                data=data,
                                )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(style("Error: " + response.json()['error'], fg="red", bold=True))
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)
    response_json = response.json()
    if validate_token(response_json):
        echo(style("\nYour file was successfully submitted.\n",
                   fg="green", bold=True))


def pretty_print_submission_details(submission):
    """
    Pretty prints details of submission
    """
    team_title = "\n{}".format(style(submission['participant_team_name'],
                                     bold=True, fg="green"))
    sid = "Submission ID: {}\n".format(style(str(submission['id']),
                                       bold=True, fg="blue"))
    title = "{} {}".format(team_title, sid)

    status = style("\nSubmission Status : {}\n".format(submission['status']), bold=True)
    execution_time = style("\nSubmission Status : {}\n".format(submission['execution_time']), bold=True)
    submitted_at = style("\nSubmission Status : {}\n".format(submission['submitted_at'].split('T')[0]), bold=True)
    phase = "{}{}{}{}".format(title, status, execution_time, submitted_at)
    echo(phase)


def display_submission_details(submission_id):
    """
    Function to fetch the details of a particular submission
    """
    url = "{}{}".format(API_HOST_URL, URLS.submission.value)
    url = url.format(submission_id)
    headers = get_request_header()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        echo(style("Error: " + response.json()['error'], fg="red", bold=True))
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)

    response_json = response.json()

    if validate_token(response_json):
        pretty_print_submission_details(response_json)
