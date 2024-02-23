import json
import os
import responses

from beautifultable import BeautifulTable
from click.testing import CliRunner
from termcolor import colored

from evalai.challenges import challenge, challenges
from evalai.set_host import host
from evalai.utils.auth import get_host_url
from evalai.login import login
from evalai.utils.urls import URLS
from evalai.utils.config import (
    API_HOST_URL,
    AUTH_TOKEN_DIR,
    AUTH_TOKEN_FILE_NAME,
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


class TestGetUserAuthTokenByLogin(BaseTestClass):

    token_file = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

    def setup(self):
        with open(self.token_file) as fo:
            self.token = fo.read()
        os.remove(self.token_file)

        valid_token_data = json.loads(challenge_response.valid_token)

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(get_host_url(), URLS.login.value),
            json=valid_token_data,
            status=200,
        )

    def teardown(self):
        with open(self.token_file, "w") as f:
            f.write(self.token)

    @responses.activate
    def test_get_user_auth_token_by_login_success(self):
        expected = "username: test"
        expected = "{}\n{}".format(
            expected,
            "Enter password: "
        )
        expected = "{}\n{}".format(
            expected,
            "\nLogged in successfully!"
        )
        runner = CliRunner()
        result = runner.invoke(login, input="test\npassword",)
        response = result.output.rstrip()
        assert response == expected


class TestGetUserAuthTokenByLoginWithHTTPError(BaseTestClass):

    token_file = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

    def setup(self):
        with open(self.token_file) as fo:
            self.token = fo.read()
        os.remove(self.token_file)

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(get_host_url(), URLS.login.value),
            status=406,
        )

    def teardown(self):
        with open(self.token_file, "w") as f:
            f.write(self.token)

    @responses.activate
    def test_get_user_auth_token_by_login_when_http_error(self):
        expected = "username: test"
        expected = "{}\n{}".format(
            expected,
            "Enter password: "
        )
        expected = "{}\n{}".format(
            expected,
            "\nUnable to log in with provided credentials."
        )
        runner = CliRunner()
        result = runner.invoke(login, input="test\npassword",)
        response = result.output.rstrip()
        assert response == expected


class TestGetUserAuthTokenByLoginWithRequestError(BaseTestClass):

    token_file = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

    def setup(self):
        with open(self.token_file) as fo:
            self.token = fo.read()
        os.remove(self.token_file)

    def teardown(self):
        with open(self.token_file, "w") as f:
            f.write(self.token)

    @responses.activate
    def test_get_user_auth_token_by_login_when_request_error(self):
        expected = "username: test"
        expected = "{}\n{}".format(
            expected,
            "Enter password: "
        )
        expected = "{}\n{}".format(
            expected,
            "\nCould not establish a connection to EvalAI."
            " Please check the Host URL.",
        )
        runner = CliRunner()
        result = runner.invoke(login, input="test\npassword",)
        response = result.output.rstrip()
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
            "The CLI would be using https://eval.ai as the default url.\n"
        )
        runner = CliRunner()
        result = runner.invoke(host)
        assert expected == result.output
        assert result.exit_code == 0

    def test_set_host_wrong_url(self):
        expected = (
            "Sorry, please enter a valid url.\n" "Example: https://eval.ai\n"
        )
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "https:/evalai.cloudcv"])
        assert expected == result.output
        assert result.exit_code == 0

    def test_set_host_url(self):
        expected = "{} is set as the host url.\n".format("https://eval.ai")
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "https://eval.ai"])
        assert expected == result.output
        assert result.exit_code == 0

    def test_set_host_url_and_display(self):
        expected = "https://eval.ai is the Host URL of EvalAI.\n"
        runner = CliRunner()
        runner.invoke(host, ["-sh", "https://eval.ai"])
        result = runner.invoke(host)
        assert expected == result.output
        assert result.exit_code == 0


class TestSetAndLoadHostURL(BaseTestClass):
    def setup(self):

        challenge_data = json.loads(challenge_response.challenges)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format("https://eval.ai", URLS.challenge_list.value),
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
            table.append_row(
                [
                    colored(values[0], "white"),
                    colored(values[1], "yellow"),
                    colored(values[2], "cyan"),
                    colored(values[3], "white"),
                    colored(values[4], "green"),
                    colored(values[5], "red"),
                ]
            )
        self.output = str(table)

    def teardown(self):
        if os.path.exists(HOST_URL_FILE_PATH):
            os.remove(HOST_URL_FILE_PATH)

    @responses.activate
    def test_set_and_load_host_url(self):
        runner = CliRunner()
        result = runner.invoke(host, ["-sh", "https://eval.ai"])
        result = runner.invoke(challenges)
        response = result.output.strip()
        assert str(response) == self.output
