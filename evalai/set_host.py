import click
import os

from click import echo, style

from evalai.utils.auth import get_host_url, validate_and_write_host_url_to_file
from evalai.utils.config import HOST_URL_FILE_PATH


@click.group(invoke_without_command=True)
@click.option(
    "-sh", "--set-host", help="Set the Host URL of the EvalAI Instance."
)
def host(set_host):
    """
    View and configure the Host URL.
    """
    if set_host is not None:
        validate_and_write_host_url_to_file(set_host)
    else:
        if not os.path.exists(HOST_URL_FILE_PATH):
            echo(
                style(
                    "You haven't configured a Host URL for the CLI.\n"
                    "The CLI would be using https://evalapi.cloudcv.org as the default url.",
                    bold=True,
                )
            )
        else:
            current_host_url = get_host_url()
            echo(
                style(
                    "{} is the Host URL of EvalAI.".format(current_host_url),
                    bold=True,
                )
            )
