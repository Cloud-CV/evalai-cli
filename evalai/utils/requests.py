import requests
import sys

from click import echo, style

from evalai.utils.config import EVALAI_ERROR_CODES
from evalai.utils.common import validate_token

from .auth import get_request_header, get_host_url


def make_request(path, method, files=None, data=None):
    if method in ["PUT", "PATCH", "DELETE"]:
        raise Exception("HTTP method {} is not supported by make_request".format(method))

    url = "{}{}".format(get_host_url(), path)
    headers = get_request_header()

    if method == "POST":
        files = {"input_file": open(files, "rb")} if files else None
        data = {"status": "submitting"}

    try:
        response = requests.request(method, url, data=data, headers=headers, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError) and response.status_code in EVALAI_ERROR_CODES:
            validate_token(response.json())
            e = response.json().get("error")  # In this case, the error message is returned by the server
        echo("Could not establish a connection to EvalAI with error: {}".format(e))
        sys.exit(1)

    if method == "POST":
        echo(
            style(
                "\nYour docker file is successfully submitted.\n",
                fg="green",
                bold=True,
            )
        )
        echo(
            style(
                "You can use `evalai submission {}` to view this submission's status.\n".format(
                    response.json().get("id")
                ),
                bold=True,
            )
        )
    return response.json()
