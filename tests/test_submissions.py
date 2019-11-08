import json
import responses
import os

from click.testing import CliRunner
from datetime import datetime
from dateutil import tz

from evalai.challenges import challenge
from evalai.submissions import submission, download_file
from tests.data import submission_response

from evalai.utils.config import API_HOST_URL
from evalai.utils.urls import URLS
from .base import BaseTestClass


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


class TestDownloadFile(BaseTestClass):
    def setup(self):
        '''
        #TODO Holding until responses doesn;t support multipart/form-data
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.download_file.value).format(
            "submission_9",
            "result"
            ),
            json=self.file,
            content_type="multipart/form-data",
            status=200,
        )
        '''
        pass

    def teardown(self):
        if os.path.exists("./result"):
            os.remove("./result")

    @responses.activate
    def test_download_file_when_url_invalid(self):
        expected = "\nThe url doesn't match the EvalAI url. Please check the url.\n\n"

        runner = CliRunner()

        result = runner.invoke(download_file, ["https://falseurl.com"])
        response = result.output
        assert response == expected

    @responses.activate
    def test_download_file_when_bucket_or_key_missing(self):
        expected = "\nThe bucket or key is missing in the url.\n\n"

        runner = CliRunner()

        result = runner.invoke(
            download_file,
            [API_HOST_URL + "/api/jobs/submission_files/?bucket=submission_9"])
        response = result.output
        assert response == expected

    @responses.activate
    def test_download_file_when_cannot_connect_EvalAI(self):
        expected = "\nCould not connect to EvalAI API. Please check" \
            " the URL or if server is running\n\n"

        runner = CliRunner()

        result = runner.invoke(
            download_file,
            [API_HOST_URL + "/api/jobs/submissio_files/?bucket=submission_9&key=result"])
        response = result.output
        assert response == expected

    '''
    @responses.activate
    def test_download_file_when_download_success(self):
        expected = "\nYour file {} is successfully downloaded.\n".format(
            "result.json"
        )
        runner = CliRunner()

        result = runner.invoke(download_file,
            [API_HOST_URL + "/api/jobs/submission_files/?bucket=submission_9&key=result"])
        response = result.output
        assert response == expected
    '''


class TestMakeSubmission(BaseTestClass):
    def setup(self):
        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            json=self.submission,
            status=200,
        )

    @responses.activate
    def test_make_submission_when_file_is_not_valid(self):
        expected = (
            "Usage: challenge phase submit [OPTIONS]\n"
            '\nError: Invalid value for "--file": Could not open file: file: No such file or directory\n'
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge, ["1", "phase", "2", "submit", "--file", "file"]
        )
        response = result.output
        assert response == expected

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
