import json
import responses

from click.testing import CliRunner
from datetime import datetime

from evalai.challenges import challenge
from evalai.submissions import submission
from tests.data import submission_response

from evalai.utils.challenges import API_HOST_URL
from evalai.utils.urls import URLS
from .base import BaseTestClass


class TestGetSubmissionDetails(BaseTestClass):

    def setup(self):

        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
                      json=self.submission, status=200)

    @responses.activate
    def test_display_submission_details(self):
        team_title = "\n{}".format(self.submission['participant_team_name'])
        sid = "Submission ID: {}\n".format(str(self.submission['id']))

        team = "{} {}".format(team_title, sid)

        status = "\nSubmission Status : {}\n".format(self.submission['status'])
        execution_time = "\nExecution Time (sec) : {}\n".format(self.submission['execution_time'])
        date = datetime.strptime(self.submission['submitted_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        date = date.strftime('%D %r')
        submitted_at = "\nSubmitted At : {} {}\n".format(date, "UTC")
        submission_data = "{}{}{}{}\n".format(team, status, execution_time, submitted_at)

        runner = CliRunner()
        result = runner.invoke(submission, ['9'])
        response = result.output
        assert response == submission_data

    @responses.activate
    def test_display_submission_details_with_a_string_argument(self):
        expected = ("Usage: submission [OPTIONS] SUBMISSION COMMAND [ARGS]...\n"
                    "\nError: Invalid value for \"SUBMISSION\": two is not a valid integer\n")
        runner = CliRunner()
        result = runner.invoke(submission, ['two'])
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_submission_details_with_no_argument(self):
        expected = ("Usage: submission [OPTIONS] SUBMISSION COMMAND [ARGS]...\n"
                    "\nError: Missing argument \"SUBMISSION\".\n")
        runner = CliRunner()
        result = runner.invoke(submission)
        response = result.output
        assert response == expected


class TestMakeSubmission(BaseTestClass):

    def setup(self):
        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(responses.POST, url.format(API_HOST_URL, URLS.make_submission.value).format("1", "2"),
                      json=self.submission, status=200)

    @responses.activate
    def test_make_submission_when_file_is_not_valid(self):
        expected = ("Usage: challenge phase submit [OPTIONS] FILE\n"
                    "\nError: Invalid value for \"FILE\": Could not open file: file: No such file or directory\n")
        runner = CliRunner()
        result = runner.invoke(challenge, ['1', 'phase', '2', 'submit', 'file'])
        response = result.output
        assert response == expected

    @responses.activate
    def test_make_submission_is_valid(self):
        expected = ("Your file {} with the ID {} was successfully submitted.".format("test_file.txt", "9"))

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('test_file.txt', 'w') as f:
                f.write('1 2 3 4 5 6')

            result = runner.invoke(challenge, ['1', 'phase', '2', 'submit', "test_file.txt"])
            assert result.exit_code == 0
            assert result.output.strip() == expected
