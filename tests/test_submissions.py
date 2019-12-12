import json
import responses
import os
from click.testing import CliRunner
from datetime import datetime
from dateutil import tz
from evalai.challenges import challenge
from evalai.submissions import submission
from tests.data import submission_response
from evalai.utils.submissions import convert_bytes_to
from evalai.utils.config import API_HOST_URL, HOST_URL_FILE_PATH
from evalai.utils.urls import URLS
from tests.base import BaseTestClass


class TestGetSubmissionDetails(BaseTestClass):
    def setup(self):

        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
            json=self.submission,
            status=200,
        )
        responses.add(
            responses.GET,
            self.submission["submission_result_file"],
            json=json.loads(submission_response.submission_result_file),
            status=200,
        )
        responses.add(
            responses.GET,
            url.format("http:/1234", URLS.get_submission.value.format("7")),
            json=json.loads(submission_response.submission_result_file),
            status=500,
        )

    @responses.activate
    def test_display_submission_result_with_missing_schema(self):
        expected = "The Submission is yet to be evaluated."
        runner = CliRunner()
        if not os.path.exists(HOST_URL_FILE_PATH):
            f = open(HOST_URL_FILE_PATH, "w")
            f.write("http:/1234")
            f.close()
        result = runner.invoke(submission, ["7", "result"])
        response = result.output.strip()
        if os.path.exists(HOST_URL_FILE_PATH):
            os.remove(HOST_URL_FILE_PATH)
        assert response == expected

    @responses.activate
    def test_display_submission_details(self):
        team_title = "\n{}".format(self.submission["participant_team_name"])
        sid = "Submission ID: {}\n".format(str(self.submission["id"]))

        team = "{} {}".format(team_title, sid)

        status = "\nSubmission Status : {}\n".format(self.submission["status"])
        execution_time = "\nExecution Time (sec) : {}\n".format(
            self.submission["execution_time"]
        )

        date = datetime.strptime(
            self.submission["submitted_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date = date.replace(tzinfo=from_zone)
        converted_date = date.astimezone(to_zone)

        date = converted_date.strftime("%D %r")
        submitted_at = "\nSubmitted At : {}\n".format(date)
        submission_data = "{}{}{}{}\n".format(
            team, status, execution_time, submitted_at
        )

        runner = CliRunner()
        result = runner.invoke(submission, ["9"])
        response = result.output
        assert response == submission_data

    @responses.activate
    def test_display_submission_details_with_a_string_argument(self):
        expected = (
            "Usage: submission [OPTIONS] SUBMISSION_ID COMMAND [ARGS]...\n"
            '\nError: Invalid value for "SUBMISSION_ID": two is not a valid integer\n'
        )
        runner = CliRunner()
        result = runner.invoke(submission, ["two"])
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_submission_details_with_no_argument(self):
        expected = (
            "Usage: submission [OPTIONS] SUBMISSION_ID COMMAND [ARGS]...\n"
            '\nError: Missing argument "SUBMISSION_ID".\n'
        )
        runner = CliRunner()
        result = runner.invoke(submission)
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_submission_result(self):
        expected = "{}\n".format(submission_response.submission_result_file).strip()
        runner = CliRunner()
        result = runner.invoke(submission, ["9", "result"])
        response = result.output.strip()
        assert response == expected

class TestMakeSubmission(BaseTestClass):
    def setup(self):
        self.submission = json.loads(submission_response.submission_result)
        bad_request_error_data = json.loads(submission_response.bad_request_error)
        unauthorized_error_data = json.loads(submission_response.unauthorized_error)
        not_acceptable_error_data = json.loads(submission_response.not_acceptable_error)

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            json=self.submission,
            status=200,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.my_submissions.value).format("3", "4"),
            json=bad_request_error_data,
            status=400,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.my_submissions.value).format("5", "6"),
            json=unauthorized_error_data,
            status=401,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.my_submissions.value).format("7", "8"),
            json=not_acceptable_error_data,
            status=406,
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format("9", "10"),
            json=self.submission,
            status=416,
        )

    @responses.activate
    def test_make_submission_when_file_is_not_valid(self):
        expected = (
            "Usage: challenge phase submit [OPTIONS]\n"
            '\nError: Invalid value for "--file": Could not open file: file: No such file or directory\n'
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge, ["9", "phase", "10", "submit", "--file", "file"]
        )
        response = result.output
        assert response == expected

    @responses.activate
    def test_make_submission_receive_other_http_error(self):
        expected = (
            self.submission["input_file"][0]
        )
        expected = (
            "416 Client Error: Requested Range Not Satisfiable for url: https://evalapi.cloudcv.org/api/jobs/challenge/9/challenge_phase/10/submission/\n{}"
        ).format(expected)
        expected = "Do you want to include the Submission Details? [y/N]: N\n{}".format(
            expected
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["9", "phase", "10", "submit", "--file", "test_file.txt"],
                input="N",
            )
            assert result.exit_code == 1
            assert result.output.strip() == expected


    @responses.activate
    def test_make_submission_when_file_is_valid_without_metadata(self):
        expected = (
                "Your file {} with the ID {} is successfully submitted.\n\n"
                "You can use `evalai submission {}` to view this submission's status."
        ).format("test_file.txt", "9", "9")
        expected = "Do you want to include the Submission Details? [y/N]: N\n\n{}".format(
            expected
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="N",
            )
            assert result.exit_code == 0
            assert result.output.strip() == expected

    @responses.activate
    def test_make_submission_when_file_is_valid_with_metadata(self):
        expected = "Do you want to include the Submission Details? [y/N]: Y"
        expected = "{}\n{}".format(
            expected,
            (
                "Method Name []: Test\nMethod Description []: "
                "Test\nProject URL []: Test\nPublication URL []: Test\n"
            ),
        )
        expected = "{}\n{}".format(
            expected,
            (
                "Your file {} with the ID {} is successfully submitted.\n\n"
                "You can use `evalai submission {}` to view this "
                "submission's status."
            ).format("test_file.txt", "9", "9"),
        )

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="Y\nTest\nTest\nTest\nTest",
            )
            assert result.exit_code == 0
            assert result.output.strip() == expected

    @responses.activate
    def test_get_my_submissions_when_http_error_406(self):
        expected = (
            "\nError: Not Acceptable\n"
            "\nUse `evalai challenges` to fetch the active challenges.\n"
            "\nUse `evalai challenge CHALLENGE phases` to fetch the "
            "active phases.\n\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge,
            ["7", "phase", "8", "submissions"]
        )
        assert result.output == expected

    @responses.activate
    def test_get_my_submissions_when_http_error_401(self):
        expected = (
            "\nError: Unauthorized\n"
            "\nUse `evalai challenges` to fetch the active challenges.\n"
            "\nUse `evalai challenge CHALLENGE phases` to fetch the "
            "active phases.\n\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge,
            ["5", "phase", "6", "submissions"]
        )
        assert result.output == expected

    @responses.activate
    def test_get_my_submissions_when_http_error_400(self):
        expected = (
            "\nError: Bad Request\n"
            "\nUse `evalai challenges` to fetch the active challenges.\n"
            "\nUse `evalai challenge CHALLENGE phases` to fetch the "
            "active phases.\n\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge,
            ["3", "phase", "4", "submissions"]
        )
        assert result.output == expected


class TestConvertBytesTo(BaseTestClass):
    def test_convert_bytes_to_kb(self):
        assert convert_bytes_to(1024, "kb") == 1

    def test_convert_bytes_to_mb(self):
        assert convert_bytes_to(1024 * 1024, "mb") == 1

    def test_convert_bytes_to_gb(self):
        assert convert_bytes_to(1024 * 1024 * 1024, "gb") == 1

    def test_convert_bytes_to_tb(self):
        assert convert_bytes_to(1024 * 1024 * 1024 * 1024, "tb") == 1

    def test_convert_bytes_to_pb(self):
        assert convert_bytes_to(1024 * 1024 * 1024 * 1024 * 1024, "pb") == 1

    def test_convert_bytes_to_eb(self):
        assert convert_bytes_to(1024 * 1024 * 1024 * 1024 * 1024 * 1024, "eb") == 1
