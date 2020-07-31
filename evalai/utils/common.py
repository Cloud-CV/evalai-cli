import os
import click
import random
import requests
import string
import sys

from bs4 import BeautifulSoup
from click import echo, style
from datetime import datetime
from dateutil import tz
from http import HTTPStatus


class Date(click.ParamType):
    """
    Date object parsed using datetime.
    """

    name = "date"

    def __init__(self, format):
        self.format = format

    def convert(self, value, param, ctx):
        try:
            date = datetime.strptime(value, self.format)
            return date
        except ValueError:
            raise self.fail(
                "Incorrect date format, please use {} format. Example: 8/23/17.".format(
                    self.format
                )
            )


def upload_with_presigned_url(file_name, presigned_url):
    """
    Function to upload a file, given the target presigned s3 url

    Arguments:
        file_name (str) -- the path of the file to be uploaded
        presigned_url (str) -- the presigned url to upload the file on s3
    """
    echo(
        style(
            "Uploading the submission file...",
            fg="green",
            bold=False,
        )
    )

    with open(os.path.realpath(file_name), 'rb') as f:
        try:
            response = requests.put(
                presigned_url,
                data=f
            )
            return response
        except Exception as err:
            echo("There was an error while uploading the file: {}".format(err))
            sys.exit(1)
        if response.status_code is not HTTPStatus.OK:
            echo("There was an error while uploading the file: ")
            response.raise_for_status()


def validate_token(response):
    """
    Function to check if the authentication token provided by user is valid or not.
    """
    if "detail" in response:
        if response["detail"] == "Invalid token":
            echo(
                style(
                    "\nThe authentication token you are using isn't valid."
                    " Please generate it again.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        if response["detail"] == "Token has expired":
            echo(
                style(
                    "\nSorry, the token has expired. Please generate it again.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)


def validate_date_format(date):
    for date_format in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(date, date_format)
        except ValueError:
            pass
    raise ValueError("Invalid date format. Please check again.")


def convert_UTC_date_to_local(date):
    # Format date
    date = validate_date_format(date)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Convert to local timezone from UTC.
    date = date.replace(tzinfo=from_zone)
    converted_date = date.astimezone(to_zone)
    date = converted_date.strftime("%D %r")
    return date


def clean_data(data):
    """
    Strip HTML and clean spaces
    """
    data = BeautifulSoup(data, "lxml").text.strip()
    data = " ".join(data.split()).encode("utf-8")
    return data


def notify_user(message, color="green", bold=False):
    echo(style(message, fg=color, bold=bold))


def generate_random_string(length):
    letter_set = string.ascii_lowercase + string.digits
    return "".join(random.choice(letter_set) for _ in range(length))
