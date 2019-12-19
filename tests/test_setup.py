import json
import mock
import sys

from click.testing import CliRunner

from evalai.setup import ignite
from evalai.utils.auth import get_host_url
from .base import BaseTestClass


class TestSetup(BaseTestClass):
    def setup(self):
        self.username = "testuser"
        self.password = "testpass"
        self.token = "validtoken" * 4  # length = 40
        self.token_json = json.dumps({"token": self.token})
        self.current_host = get_host_url()
        self.new_host = "http://testserver"
        self.login_failure = "\nLogin failed."
        self.login_success = "\nLogged in successfully!"
        self.setup_success = "\nSetup successful!"
        self.revert_host = "Reverting host URL from {} to {}"
        self.set_host_failure = "Couldn't set host URL to {}\nCurrent host URL: {}"
        self.login_args = ["--username", self.username, "--password", self.password]
        self.login_args_with_new_host = self.login_args.extend(["--host", self.new_host])
        self.login_args_with_current_host = self.login_args.extend(["--host", self.current_host])

    @mock.patch("evalai.setup.write_json_auth_token_to_file")
    @mock.patch("evalai.setup.get_user_auth_token_by_login")
    def test_setup_only_login_success(self, mock_get_token_by_login, mock_write_json_token_to_file):
        mock_get_token_by_login.return_value = self.token_json

        runner = CliRunner()
        result = runner.invoke(ignite, self.login_args)
        expected = "{}\n{}\n".format(self.login_sucess, self.setup_success)

        mock_get_token_by_login.assert_called_with(username=self.username, password=self.password)
        mock_write_json_token_to_file.assert_called_with(self.token_json)
        assert result.exit_code == 0
        assert result.output == expected

    @mock.patch("evalai.setup.validate_and_write_host_url_to_file")
    @mock.patch("evalai.setup.write_json_auth_token_to_file")
    @mock.patch("evalai.setup.get_user_auth_token_by_login")
    def test_setup_success(self, mock_get_token_by_login, mock_write_json_token_to_file,
                           mock_val_write_host_url_to_file):
        mock_get_token_by_login.return_value = self.token_json

        runner = CliRunner()
        expected = "{}\n{}\n".format(self.login_success, self.setup_success)
        result = runner.invoke(ignite, self.login_args_with_new_host)

        ## mock_val_write_host_url_to_file.assert_called_with(self.new_host)
        mock_get_token_by_login.assert_called_with(self.username, self.password)
        mock_write_json_token_to_file.assert_called_with(self.token_json)
        assert result.exit_code == 0
        assert result.output == expected

    @mock.patch("evalai.setup.validate_and_write_host_url_to_file")
    def test_setup_when_set_host_fails(self, mock_val_write_host_url_to_file):
        mock_val_write_host_url_to_file.side_effect = sys.exit

        runner = CliRunner()
        expected = self.set_host_failure.format(self.new_host, self.current_host)
        result = runner.invoke(ignite, self.login_args_with_new_host)

        mock_val_write_host_url_to_file.assert_called_with(self.new_host)
        assert result.exit_code == 1
        assert result.output == expected

    @mock.patch("evalai.setup.get_user_auth_token_by_login")
    def test_setup_when_login_fails(self, mock_get_token_by_login):
        mock_get_token_by_login.side_effect = Exception

        runner = CliRunner()
        revert_host_message = self.revert_host.format(self.new_host, self.current_host)
        expected = "{}\n{}\n".format(self.login_failure, revert_host_message)
        result = runner.invoke(ignite, self.login_args_with_new_host)

        assert result.exit_code == 1
        assert expected in result.output
