import requests
import sys

from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.config import API_HOST_URL, EVALAI_ERROR_CODES
from evalai.utils.urls import URLS
from evalai.utils.common import validate_token


def submit_a_file(challenge_id, phase_id, file):
    """
    Function to create a new participant team.
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
        if (response.status_code in EVALAI_ERROR_CODES):
            validate_token(response.json())
            echo(style("Error: {}".format(response.json()["error"]), fg="red", bold=True))
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)
    response = response.json()
    echo(style("\nYour file was successfully submitted.\n",
               fg="green", bold=True))


def pretty_print_submission_details(submission):
    """
    Function to print details of a submission
    """
    team_title = "\n{}".format(style(submission['participant_team_name'],
                                     bold=True, fg="green"))
    sid = "Submission ID: {}\n".format(style(str(submission['id']),
                                       bold=True, fg="blue"))
    team = "{} {}".format(team_title, sid)

    status = style("\nSubmission Status : {}\n".format(submission['status']), bold=True)
    execution_time = style("\nSubmission Status : {}\n".format(submission['execution_time']), bold=True)
    submitted_at = style("\nSubmission Status : {}\n".format(submission['submitted_at'].split('T')[0]), bold=True)
    phase = "{}{}{}{}".format(team, status, execution_time, submitted_at)
    echo(phase)


def display_submission_details(submission_id):
    """
    Function to display details of a particular submission
    """
    url = "{}{}".format(API_HOST_URL, URLS.submission.value)
    url = url.format(submission_id)
    headers = get_request_header()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if (response.status_code in EVALAI_ERROR_CODES):
            validate_token(response.json())
            echo(style("Error: {}".format(response.json()["error"]), fg="red", bold=True))
        else:
            echo(err)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        echo(err)
        sys.exit(1)
    response = response.json()

    pretty_print_submission_details(response)
