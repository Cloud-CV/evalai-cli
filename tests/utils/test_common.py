import os

from click.testing import CliRunner
from evalai.login import login
from evalai.utils.config import (
    AUTH_TOKEN_DIR,
    AUTH_TOKEN_FILE_NAME,
)
from unittest.mock import patch

from ..base import BaseTestClass


@patch("evalai.login.get_user_auth_token_by_login")
class TestStoreDataToJson(BaseTestClass):
    def setup(self):
        token_file = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

        with open(token_file) as f:
            self.token = f.read()

    def test_store_data_to_json(self, mock_get_user_auth_token_by_login):
        mock_get_user_auth_token_by_login.return_value = self.token

        expected = "\n\nLogged in successfully!"
        runner = CliRunner()
        result = runner.invoke(login, input="username\npassword")
        response = result.output
        assert expected in response

    @patch("evalai.utils.common.json.dump")
    def test_store_data_to_json_when_error_is_raised(self, mock_dump, mock_get_user_auth_token_by_login):
        mock_get_user_auth_token_by_login.return_value = self.token
        error = "Exception"
        mock_dump.side_effect = OSError(error)

        expected = "Unable to store token data due to error: {}".format(error)
        runner = CliRunner()
        result = runner.invoke(login, input="username\npassword")
        response = result.output
        assert expected in response
