import responses
import os

from unittest.mock import patch
from click.testing import CliRunner
from evalai.utils.auth import URLS
from evalai.utils.config import (
    API_HOST_URL,
    AUTH_TOKEN_DIR,
    AUTH_TOKEN_FILE_NAME
)
from evalai.login import login

from .base import BaseTestClass


class TestLogin(BaseTestClass):
    def setup(self):
        with open(os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)) as f:
            token = f.read()

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.login.value),
            json=token,
            status=200,
        )

    @responses.activate
    @patch("evalai.utils.common.json.dump")
    def test_login_when_storing_json_fails(self, mock_dump):
        error = "Exception"
        expected = "Unable to store token data due to error: {}".format(error)
        mock_dump.side_effect = OSError(error)

        runner = CliRunner()
        result = runner.invoke(login, input="username\npassword")
        response = result.output
        assert expected in response
