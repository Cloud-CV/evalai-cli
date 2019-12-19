import click
import json
import mock
import os
import responses

from beautifultable import BeautifulTable
from click.testing import CliRunner
from termcolor import colored

from evalai.challenges import challenge, challenges
from evalai.set_host import host
from evalai.utils.auth import (
    write_host_url_to_file,
    write_auth_token_to_file,
    write_json_auth_token_to_file,
)
from evalai.utils.urls import URLS
from evalai.utils.config import (
    API_HOST_URL,
    AUTH_TOKEN_DIR,
    AUTH_TOKEN_FILE_NAME,
    AUTH_TOKEN_PATH,
    HOST_URL_FILE_PATH,
)
from evalai.utils.common import convert_UTC_date_to_local

from tests.data import challenge_response
from tests.base import BaseTestClass


class TestGetUserAuthToken(BaseTestClass):

    token_file = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

    def setup(self):
        with open(self.token_file) as fo:
            self.token = fo.read()
        os.remove(self.token_file)

    def teardown(self):
        with open(self.token_file, "w") as f:
            f.write(self.token)

    def test_get_user_auth_token_when_file_does_not_exist(self):
        expected = (
            "\nThe authentication token json file doesn't exists at the required path. "
            "Please download the file from the Profile section of the EvalAI webapp and "
            "place it at ~/.evalai/token.json\n\n"
        )
        runner = CliRunner()
        result = runner.invoke(challenges)
        response = result.output
        assert response == expected


class TestUserRequestWithInvalidToken(BaseTestClass):
    def setup(self):

        invalid_token_data = json.loads(challenge_response.invalid_token)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            json=invalid_token_data,
            status=401,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.host_teams.value),
            json=invalid_token_data,
            status=401,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.leaderboard.value).format("1"),
            json=invalid_token_data,
            status=401,
        )

        self.expected = "\nThe authentication token you are using isn't valid. Please generate it again.\n\n"

    @responses.activate
    def test_display_all_challenge_lists_when_token_is_invalid(self):
        runner = CliRunner()
        result = runner.invoke(challenges)
        response = result.output
        assert response == self.expected

    @responses.activate
    def test_display_leaderboard_when_token_is_invalid(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "leaderboard", "1"])
        response = result.output
        assert response == self.expected

    @responses.activate
    def test_display_participant_challenge_lists_when_token_is_invalid(self):
        expected = "The authentication token you are using isn't valid. Please generate it again."
        runner = CliRunner()
        result = runner.invoke(challenges, ["--host"])
        response = result.output.strip()
        assert response == expected


class TestUserRequestWithExpiredToken(BaseTestClass):
    def setup(self):

        token_expired_data = json.loads(challenge_response.token_expired)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            json=token_expired_data,
            status=401,
        )

    @responses.activate
    def test_display_all_challenge_lists_when_token_has_expired(self):
        expected = (
            "\nSorry, the token has expired. Please generate it again.\n\n"
        )
        runner = CliRunner()
        result = runner.invoke(challenges)
        response = result.output
        assert response == expected


class TestHostConfig(BaseTestClass):
    def teardown(self):
        if os.path.exists(HOST_URL_FILE_PATH):
            os.remove(HOST_URL_FILE_PATH)

    def test_get_default_host(self):
        expected = (
            "You haven't configured a Host URL for the CLI.\n"
            "The CLI would be using https://evalapi.cloudcv.org as the default url.\n"
        )
        runner = CliRunner()
        result = runner.invoke(host)
        assert expected == result.output
        assert result.exit_code == 0

    def test_set_host_wrong_url(self):
        expected = (
            "Sorry, please enter a valid url.\n"
            "Example: https://evalapi.cloudcv.org"
        )
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "http:/evalapi.cloudcv"])
        assert expected == result.output.strip('None\n')  # The None\n because sys.exit creates an empty new line.
        assert result.exit_code == 0

    def test_set_host_url(self):
        expected = "{} is set as the host url.\n".format(
            "https://evalapi.cloudcv.org"
        )
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "https://evalapi.cloudcv.org"])
        assert expected == result.output
        assert result.exit_code == 0

    def test_set_host_url_and_display(self):
        expected = "https://evalapi.cloudcv.org is the Host URL of EvalAI.\n"
        runner = CliRunner()
        runner.invoke(host, ["-sh", "https://evalapi.cloudcv.org"])
        result = runner.invoke(host)
        assert expected == result.output
        assert result.exit_code == 0


class TestSetAndLoadHostURL(BaseTestClass):
    def setup(self):

        challenge_data = json.loads(challenge_response.challenges)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(
                "https://evalapi.cloudcv.org", URLS.challenge_list.value
            ),
            json=challenge_data,
            status=200,
        )

        self.output = ""
        challenge_data = challenge_data["results"]
        table = BeautifulTable(max_width=200)
        attributes = ["id", "title", "short_description"]
        columns_attributes = [
            "ID",
            "Title",
            "Short Description",
            "Creator",
            "Start Date",
            "End Date",
        ]
        table.column_headers = columns_attributes
        for challenge_json in reversed(challenge_data):
            values = list(map(lambda item: challenge_json[item], attributes))
            creator = challenge_json["creator"]["team_name"]
            start_date = convert_UTC_date_to_local(
                challenge_json["start_date"]
            )
            end_date = convert_UTC_date_to_local(challenge_json["end_date"])
            values.extend([creator, start_date, end_date])
            table.append_row([colored(values[0], 'white'),
                              colored(values[1], 'yellow'),
                              colored(values[2], 'cyan'),
                              colored(values[3], 'white'),
                              colored(values[4], 'green'),
                              colored(values[5], 'red'),
                              ])
        self.output = str(table)

    def teardown(self):
        if os.path.exists(HOST_URL_FILE_PATH):
            os.remove(HOST_URL_FILE_PATH)

    @responses.activate
    def test_set_and_load_host_url(self):
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "https://evalapi.cloudcv.org"])
        result = runner.invoke(challenges)
        response = result.output.strip()
        assert str(response) == self.output


@mock.patch("evalai.utils.auth.echo")
class TestUtilWriteHostUrlToFile(BaseTestClass):
    def setup(self):
        self.old_host = ''
        self.new_host = 'http://testserver.xyz'
        if os.path.exists(AUTH_TOKEN_DIR):
            with open(HOSt_URL_FILE_PATh, "r") as fr:
                self.old_host = fr.read()

    def teardown(self):
        if os.path.exists(HOST_URL_FILE_PATH):
            with open(HOST_URL_FILE_PATH, "w") as fw:
                fw.write(self.old_host)

    def test_write_host_url_to_file_success(self, mock_echo):
        write_host_url_to_file()
        with open(HOST_URL_FILE_PATH, "r") as fr:
            assert fr.read() == self.new_host
        mock_echo.assert_called_with(
            click.style(
                "{} is set as the host url.".format(self.new_host),
                bold=True,
            )
        )

    @mock.patch("evalai.utils.auth.__builtins__.open")
    def test_write_host_url_to_file_fail(self, mock_open, mock_echo):
        mock_fw = mock.MagicMock()
        mock_open.return_value = mock_fw
        mock_fw.write.side_effect = OSError("Permission denied")  # For example
        try:
            write_host_url_to_file()
        except SystemExit as se:
            assert str(se) == '1'  # Exit code
        mock_open.assert_called_with(HOST_URL_FILE_PATh, "w")
        mock_echo.assert_called_once_with("Permission denied")


class TestUtilWriteTokenToFile(BaseTestClass):
    def setup(self):
        self.new_token = "tokenisnew" * 4  # Length = 40
        self.new_token_json = json.dumps({"token": self.new_token})
        self.old_token = ''
        if os.path.exists(AUTH_TOKEN_PATH):
            with open(AUTH_TOKEN_PATH, "r") as fr:
                self.old_token = fr.read()

    def teardown(self):
        if os.path.exists(AUTH_TOKEN_DIR):
            with open(AUTH_TOKEN_PATH, "w") as fw:
                fw.write(self.old_token)

    def test_write_json_auth_token_to_file_success(self):
        write_json_auth_token_to_file(self.new_token_json)
        with open(AUTh_TOKEN_PATH, "r" ) as fr:
            assert fr.read() == self.new_token_json

    @mock.patch("evalai.utils.auth.echo")
    @mock.patch("evalai.utils.auth.json.dumps")
    def test_write_json_auth_token_to_file_fail(self, mock_json, mock_echo):
        try:
            mock_json.side_effect = OSError("Error description")
        except SystemExit as se:
            assert str(se) == '1'
        mock_echo.assert_called_with("Error description")

    def test_write_auth_token_to_file_success(self):
        write_auth_token_to_file(self.new_token)
        with open(AUTH_TOKEN_PATH, "r") as fr:
            assert fr.read() == self.new_token_json
