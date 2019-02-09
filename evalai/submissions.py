import click
from urllib3 import response

from evalai.utils.auth import get_host_url, get_request_header
from evalai.utils.common import (convert_UTC_date_to_local,
                                 validate_date_format, validate_token)
from evalai.utils.config import EVALAI_ERROR_CODES
from evalai.utils.requests import make_request
from evalai.utils.submissions import display_submission_details
from evalai.utils.urls import URLS


@click.group(invoke_without_command=True)
@click.argument("SUBMISSION_ID", type=int)
def submission(submission_id):
    """
    View submission specific details.
    """
    """
    Invoked by `evalai submission SUBMISSION_ID`.
    """
    display_submission_details(submission_id)


@click.group(invoke_without_command=True)
@click.argument("IMAGE[:TAG]")
@click.option("-p", "--phase", help="challenge-phase-id to which image is to be pushed")
def push(image, phase):
    """
    View submission specific details.
    """
    """
    Invoked by `evalai push IMAGE[:TAG] -p PHASE_ID`.
    """
    tag = None
    image = image.split(":")
    if len(image) == 1:
        tag = "latest"
    elif len(image) == 2:
        image, tag = image[0], image[1]

    request_path = URLS.get_aws_credentials.value
    request_path = url_path.format(phase)

    response = make_request(url_path, "GET")
    federated_user = response['success']
    print(federated_user)
    pretty_print_submission_details(federated_user)
