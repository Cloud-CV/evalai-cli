import os

import base64
import boto3
import click
import docker
import json
import requests
import shutil
import sys
import tempfile
import urllib.parse as urlparse
import uuid

from click import echo, style

from evalai.utils.common import notify_user
from evalai.utils.requests import make_request
from evalai.utils.submissions import (
    display_submission_stderr,
    convert_bytes_to,
)
from evalai.utils.urls import URLS
from evalai.utils.config import EVALAI_HOST_URLS, HOST_URL_FILE_PATH


class Submission(object):

    def __init__(self, submission_id):
        self.submission_id = submission_id


@click.group(invoke_without_command=True)
@click.argument("SUBMISSION_ID", type=int)
@click.pass_context
def submission_error(ctx, submission_id):
    """
    Display submission Error using submission id.
    """
    """
    Invoked by `evalai submission_error SUBMISSION_ID`.
    """
    ctx.obj = Submission(submission_id=submission_id)
    if ctx.invoked_subcommand is None:
        display_submission_stderr(submission_id)
