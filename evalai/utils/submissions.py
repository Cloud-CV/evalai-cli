import requests
import sys

from beautifultable import BeautifulTable
from click import echo, style

from evalai.utils.auth import get_request_header
from evalai.utils.common import validate_token
from evalai.utils.urls import URLS
from evalai.utils.config import API_HOST_URL, EVALAI_ERROR_CODES


def pretty_print_submission_table(submissions):
    """
    Funcion to print the submissions for a particular Challenge.
    """
    table = BeautifulTable()
    attributes = ["participant_team_name", "method_name", "execution_time", "status", "submitted_at"]
    table.column_headers = attributes

    for submission in submissions:
        team_name = submission["participant_team_name"]
        method_name = submission["method_name"]
        execution_time = submission["execution_time"]
        status = submission["status"]
        submitted = submission["submitted_at"].split("T")[0]
        value = [team_name, method_name, execution_time, status, submitted]
        table.append_row(value)
    echo(table)


def display_your_submissions(challenge_id, phase_id):
    """
    Function display the details of a particular submission.
    """
    url = URLS.submissions.value
    url = "{}{}".format(API_HOST_URL, url)
    url = url.format(challenge_id, phase_id)
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

    response_json = response.json()

    submissions = response_json["results"]
    pretty_print_submission_table(submissions)
