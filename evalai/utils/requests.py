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
    except requests.exceptions.HTTPError as e:
        if response.status_code in EVALAI_ERROR_CODES:
            validate_token(response.json())
            echo(
                style(
                    "\nError: {}\n".format(response.json().get("error")),
                    fg="red",
                    bold=True,
                )
            )
            echo(
                style(
                    "Use `evalai challenges` to fetch the active challenges."
                    "Use `evalai challenge CHALLENGE phases` to fetch the "
                    "active phases.",
                    bold=True,
                )
            )
        else:
            echo(e)
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
