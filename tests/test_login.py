import responses
import json

from unittest.mock import patch
from unittest import TestCase
from click.testing import CliRunner
from evalai.utils.auth import URLS
from evalai.utils.config import API_HOST_URL
from evalai.login import login

from .base import BaseTestClass


class TestLogin(TestCase):
    def setUp(self):
        token = json.loads("""{"token": "test"}""")

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
