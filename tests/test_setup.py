import mock

from click.testing import CliRunner
from functools import update_wrapper
from mock import patch

from evalai.login import login
from evalai.set_host import host as set_host
from evalai.setup import ignite
from evalai.utils.auth import get_host_url

from .base import BaseTestClass


class TestSetupConfig(BaseTestClass):
    def setup(self):
        self.username = "testuser"
        self.password = "testpass"
        self.valid_token = "validtoken" * 4  # length = 40
        self.new_token = "newertoken" * 4
        self.mock_ctx = mock.MagicMock()
        self.current_host = get_host_url()
        self.new_host = "http://127.0.0.1:8000"
        self.pass_ctx_patcher = patch("evalai.setup.click.pass_context", self.mock_pass_ctx_decorator)
        self.pass_ctx_patcher.start()

    def teardown(self):
        self.mock_ctx.reset_mock()
        self.pass_ctx_patcher.stop()

    def mock_pass_ctx_decorator(self, f):
        def new_func(*args, **kwargs):
            return f(self.mock_ctx, *args, **kwargs)
        return update_wrapper(new_func, f)

    @patch("evalai.setup.get_user_auth_token_by_login")
    @patch("evalai.setup.get_user_auth_token")
    def test_setup_login_only_success(self, mock_get_token, mock_get_token_by_login):
        mock_get_token.return_value = self.valid_token
        mock_get_token_by_login.return_value = self.valid_token
        runner = CliRunner()

        with self.mock_ctx.invoke as mock_invoke:
            result = runner.invoke(
                ignite, username=self.username, password=self.password,
            )
            mock_get_token_by_login.assert_called_with(username=self.username, password=self.password)
            mock_invoke.assert_called_with(login, username=self.username, password=self.password)

        assert result.exit_code == 0
        assert result.output.endswith('Setup successful.\n')

    @patch("evalai.setup.get_user_auth_token_by_login")
    @patch("evalai.setup.get_user_auth_token")
    @patch("evalai.setup.get_host_url")
    def test_setup_success(self, mock_get_host, mock_get_token, mock_get_token_by_login):
        mock_get_token.return_value = self.valid_token
        mock_get_token_by_login.return_value = self.valid_token
        mock_get_host.return_value = self.new_host
        runner = CliRunner()

        with self.mock_ctx.invoke as mock_invoke:
            result = runner.invoke(
                ignite, username=self.username, password=self.password, host=self.new_host,
            )
            mock_invoke.assert_any_call(set_host, set_host=self.new_host)
            mock_invoke.assert_called_with(login, username=self.username, password=self.password)

        assert result.exit_code == 0
        assert result.output.endswith('Setup successful.\n')

    @patch("evalai.setup.get_host_url")
    def test_setup_when_set_host_fails(self, mock_get_host):
        mock_get_host.return_value = self.current_host
        runner = CliRunner()

        with self.mock_ctx.invoke as mock_invoke:
            result = runner.invoke(
                ignite, username=self.username, password=self.password, host=self.new_host,
            )
            mock_invoke.assert_called_once_with(set_host, set_host=self.new_host)

        message1 = "Couldn't set host URL to {}".format(self.new_host)
        message2 = "Current host URL: {}".format(self.current_host)
        expected = "{}\n{}\n".format(message1, message2)
        assert result.exit_code == 1
        assert expected in result.output

    @patch("evalai.setup.get_user_auth_token_by_login")
    @patch("evalai.setup.get_user_auth_token")
    @patch("evalai.setup.get_host_url")
    def test_setup_when_login_fails(self, mock_get_host, mock_get_token, mock_get_token_by_login):
        mock_get_host.return_value = self.new_host
        mock_get_token.return_value = self.valid_token
        mock_get_token_by_login.return_value = self.new_token
        runner = CliRunner()

        with self.mock_ctx.invoke as mock_invoke:
            result = runner.invoke(
                ignite, username=self.username, password=self.password, host=self.new_host,
            )
            mock_invoke.assert_any_call(set_host, set_host=self.new_host)
            mock_invoke.assert_any_call(login, username=self.username, password=self.password)
            mock_invoke.assert_called_with(set_host, set_host=self.current_host)

        message1 = "Login failed."
        message2 = "Reverting host URL from {0} to {1}".format(self.new_host, self.current_host)
        expected = "{}\n{}\n".format(message1, message2)
        assert result.exit_code == 1
        assert expected in result.output
