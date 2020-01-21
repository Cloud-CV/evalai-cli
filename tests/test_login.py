import responses

from unittest.mock import patch
from click.testing import CliRunner
from evalai.utils.auth import (
    get_host_url,
    URLS
)
from evalai.login import login

from .base import BaseTestClass


class TestLogin(BaseTestClass):
    def setup(self):
        payload = {"username": "username", "password": "password"}

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(get_host_url(), URLS.login.value),
            headers=payload,
            json={"token": "test"},
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
        response = result.output.rstrip()
        assert expected in response
