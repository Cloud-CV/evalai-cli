import json
import os
import responses

from click.testing import CliRunner
from requests.exceptions import RequestException

from evalai.challenges import challenge, challenges
from evalai.teams import teams
from evalai.submissions import submission
from evalai.utils.auth import get_request_header, get_host_url
from evalai.utils.urls import URLS
from evalai.utils.config import API_HOST_URL

from .base import BaseTestClass
from tests.data import challenge_response, teams_response


class TestHTTPErrorRequests(BaseTestClass):
    def setup(self):

        url = "{}{}"

        # Challenge URLS

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "1", "2"
            ),
            json=json.loads(challenge_response.challenge_phase_details),
            status=200,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.past_challenge_list.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.future_challenge_list.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_teams.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.host_teams.value),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_challenges.value).format(
                "3"
            ),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_details.value.format("1")),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.host_challenges.value).format("2"),
            status=404,
        )

        # Teams URLS

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            status=404,
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            status=404,
        )

        responses.add(
            responses.POST,
            url.format(
                API_HOST_URL, URLS.participate_in_a_challenge.value
            ).format("2", "3"),
            status=404,
        )

        # Phase URLS

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_list.value).format(
                "10"
            ),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "10", "20"
            ),
            status=404,
        )

        # Submission URLS
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.my_submissions.value).format(
                "3", "7"
            ),
            status=404,
        )
        # Leaderboard URLS
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.leaderboard.value).format("1"),
            status=404,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
            status=404,
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            status=404,
        )

        # PhaseSplit URLS
        responses.add(
            responses.GET,
            url.format(
                API_HOST_URL, URLS.challenge_phase_split_detail.value
            ).format("1"),
            status=404,
        )

        self.expected = "404 Client Error: Not Found for url: {}"

    @responses.activate
    def test_display_all_challenge_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges)
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_past_challenge_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["past"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.past_challenge_list.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_ongoing_challenge_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["ongoing"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_future_challenge_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["future"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.future_challenge_list.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_host_challenge_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--host"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.host_teams.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_participant_challenge_lists_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.participant_teams.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_participant_and_host_challenge_lists_for_http_error_404(
        self
    ):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant", "--host"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.host_teams.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_display_challenge_phase_detail_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phase", "20"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_phase_detail.value)
        expected = self.expected.format(url).format("10", "20")
        assert response == expected

    @responses.activate
    def test_display_challenge_phase_list_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phases"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_phase_list.value)
        expected = self.expected.format(url).format("10")
        assert response == expected

    @responses.activate
    def test_display_participant_team_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(teams, ["--participant"])
        response = result.output
        url = "{}{}".format(API_HOST_URL, URLS.participant_team_list.value)
        expected = "{}{}".format(self.expected.format(url), "\n")
        assert response == expected

    @responses.activate
    def test_create_team_for_http_error_404(self):
        user_prompt_text = (
            "Enter team name: TeamTest\n"
            "Please confirm the team name - TeamTest [y/N]: y\n"
            "Do you want to enter the Team URL [y/N]: N\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            teams, ["create", "participant"], input="TeamTest\ny\nN"
        )
        response = result.output
        url = "{}{}".format(API_HOST_URL, URLS.participant_team_list.value)
        expected = "{}{}".format(self.expected.format(url), "\n")
        expected = "{}{}".format(user_prompt_text, expected)
        assert response == expected

    @responses.activate
    def test_participate_in_a_challenge_for_http_error_404(self):
        terms_and_conditions_page_url = "{}{}".format(get_host_url(), URLS.terms_and_conditions_page.value)
        terms_and_conditions_page_url = terms_and_conditions_page_url.format(2)

        url = "{}{}".format(
            API_HOST_URL, URLS.participate_in_a_challenge.value
        ).format("2", "3")

        expected = (
            "Please refer challenge terms and conditions here: {}"
            "\n\nBy agreeing to participate in the challenge, you are agreeing to terms and conditions."
            "\n\nDo you accept challenge terms and conditions? [y/N]: Y\n".format(terms_and_conditions_page_url)
            + self.expected.format(url) + "\n"
        )

        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "participate", "3"], input="Y")
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_my_submission_details_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["3", "phase", "7", "submissions"])
        response = result.output
        url = "{}{}".format(API_HOST_URL, URLS.my_submissions.value).format(
            "3", "7"
        )
        expected = "{}{}".format(self.expected.format(url), "\n")
        assert response == expected

    @responses.activate
    def test_display_submission_details_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(submission, ["9"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.get_submission.value).format(
            "9"
        )
        assert response == self.expected.format(url)

    @responses.activate
    def test_make_submission_for_http_error_404(self):
        runner = CliRunner()
        url = "{}{}".format(API_HOST_URL, URLS.make_submission.value).format(
            "1", "2"
        )
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="N\nN",
            )
            response = result.output.rstrip()
            expected = (
                "Do you want to include the Submission Details? [y/N]: N\n"
                "Do you want to include the Submission Metadata? [y/N]: N\n{}".format(
                    self.expected.format(url)
                )
            )
            assert response == expected

    @responses.activate
    def test_display_challenge_phase_split_list_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["1", "phase", "2", "splits"])
        response = result.output.rstrip()
        url = "{}{}".format(
            API_HOST_URL, URLS.challenge_phase_split_detail.value
        )
        expected = self.expected.format(url).format("1")
        assert response == expected.format(url)

    @responses.activate
    def test_display_challenge_details_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["1"])
        response = result.output
        url = "{}{}".format(API_HOST_URL, URLS.challenge_details.value).format(
            "1"
        )
        expected = "{}{}".format(self.expected.format(url), "\n")
        assert response == expected

    @responses.activate
    def test_display_leaderboard_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "leaderboard", "1"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.leaderboard.value).format("1")
        expected = self.expected.format(url)
        assert response == expected


class TestCreateChallengeWhenZipFileDoesNotExist(BaseTestClass):
    def setup(self):

        response_data = """
        {
            "error": "The zip file contents cannot be extracted. Please check the format!"
        }
        """
        error_data = json.loads(response_data)
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.create_challenge.value).format("4"),
            json=error_data,
            status=406,
        )

    @responses.activate
    def test_create_challenge_when_zip_file_does_not_exist(self):

        expected = ("\nError: The zip file contents cannot be extracted. Please check the format!\n"
                    "\nUse `evalai challenges` to fetch the active challenges.\n"
                    "\nUse `evalai challenge CHALLENGE phases` to fetch the "
                    "active phases.\n\n"
                    )
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenges, ["create", "--file", "test_file.txt", "4"],
            )

            assert result.output == expected


class TestSubmissionDetailsWhenObjectDoesNotExist(BaseTestClass):
    def setup(self):

        error_data = json.loads(teams_response.object_error)
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
            json=error_data,
            status=406,
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            json=error_data,
            status=406,
        )

        # To get Challenge Phase Details
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "1", "2"
            ),
            json=json.loads(challenge_response.challenge_phase_details),
            status=200,
        )
        self.expected = "Error: Sorry, the object does not exist."

    @responses.activate
    def test_display_submission_details_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(submission, ["9"])
        response = result.output.strip()
        expected = "{}\n\n{}".format(
            self.expected,
            "Use `evalai challenge CHALLENGE "
            "phase PHASE submissions` to view your submission.",
        )
        assert response == expected

    @responses.activate
    def test_make_submission_for_object_does_not_exist(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="N\nN",
            )
            response = result.output.strip()

            expected = (
                "Do you want to include the Submission Details? [y/N]: N\n"
                "Do you want to include the Submission Metadata? [y/N]: N\n\n{}".format(
                    self.expected
                )
            )
            expected = "{}\n\n{}".format(
                expected,
                "Use `evalai challenges` to fetch the active challenges.",
            )
            expected = "{}\n\n{}".format(
                expected,
                "Use `evalai challenge CHALLENGE phases` "
                "to fetch the active phases.",
            )
            assert response == expected


class TestTeamsWhenObjectDoesNotExist(BaseTestClass):
    def setup(self):

        error_data = json.loads(teams_response.object_error)
        url = "{}{}"

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_teams.value),
            json=error_data,
            status=406,
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            json=error_data,
            status=406,
        )

        responses.add(
            responses.POST,
            url.format(
                API_HOST_URL, URLS.participate_in_a_challenge.value
            ).format("2", "3"),
            json=error_data,
            status=406,
        )
        self.expected = "Error: Sorry, the object does not exist."

    @responses.activate
    def test_display_participant_team_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(teams, ["--participant"])
        response = result.output.rstrip()
        assert response == self.expected

    @responses.activate
    def test_create_team_for_object_does_not_exist(self):
        user_prompt_text = (
            "Enter team name: TeamTest\n"
            "Please confirm the team name - TeamTest [y/N]: y\n"
            "Do you want to enter the Team URL [y/N]: N\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            teams, ["create", "participant"], input="TeamTest\ny\nN"
        )
        response = result.output.rstrip()
        expected = "{}{}".format(user_prompt_text, self.expected)
        assert response == expected

    @responses.activate
    def test_participate_in_a_challenge_when_object_does_not_exist(self):
        terms_and_conditions_page_url = "{}{}".format(get_host_url(), URLS.terms_and_conditions_page.value)
        terms_and_conditions_page_url = terms_and_conditions_page_url.format(2)
        expected = (
            "Please refer challenge terms and conditions here: {}"
            "\n\nBy agreeing to participate in the challenge, you are agreeing to terms and conditions."
            "\n\nDo you accept challenge terms and conditions? [y/N]: Y\n\n".format(terms_and_conditions_page_url)
            + self.expected
        )

        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "participate", "3"], input="Y")
        response = result.output.rstrip()
        expected = "{}\n\n{}".format(
            expected,
            "Use `evalai challenges` to fetch the active challenges.",
        )
        expected = "{}\n\n{}".format(
            expected, "Use `evalai teams` to fetch your participant teams."
        )
        assert response == expected


class TestTeamsWhenTeamNameAlreadyExists(BaseTestClass):
    def setup(self):

        error_data = json.loads(
            teams_response.participant_team_already_exists_error
        )
        url = "{}{}"

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            json=error_data,
            status=406,
        )

    @responses.activate
    def test_participate_in_a_challenge_for_team_name_exists(self):
        user_prompt_text = (
            "Enter team name: TeamTest\n"
            "Please confirm the team name - TeamTest [y/N]: y\n"
            "Do you want to enter the Team URL [y/N]: N\n"
        )
        runner = CliRunner()
        result = runner.invoke(
            teams, ["create", "participant"], input="TeamTest\ny\nN"
        )
        response = result.output.rstrip()
        expected = (
            "Error: participant team with this team name already exists."
        )
        expected = "{}{}".format(user_prompt_text, expected)
        assert response == expected


class TestDisplayChallengePhasesWhenObjectDoesNotExist(BaseTestClass):
    def setup(self):

        error_data = json.loads(challenge_response.object_error)
        url = "{}{}"

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_list.value).format(
                "10"
            ),
            json=error_data,
            status=406,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "10", "20"
            ),
            json=error_data,
            status=406,
        )

        self.expected = "Error: Sorry, the object does not exist."

    @responses.activate
    def test_display_challenge_phase_list_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phases"])
        response = result.output.rstrip()
        expected = "\n{}\n\n{}".format(
            self.expected,
            "Use `evalai challenges` to fetch the active challenges.\n"
            "\nUse `evalai challenge CHALLENGE phases` to fetch the "
            "active phases.",
        )
        assert response == expected

    @responses.activate
    def test_display_challenge_phase_detail_for_object_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phase", "20"])
        response = result.output.rstrip()
        expected = "\n{}\n\n{}".format(
            self.expected,
            "Use `evalai challenges` to fetch the active challenges.",
        )
        expected = "{}\n\n{}".format(
            expected,
            "Use `evalai challenge CHALLENGE phases` to fetch the active phases.",
        )
        assert response == expected


class TestGetParticipantOrHostTeamChallengesHTTPErrorRequests(BaseTestClass):
    def setup(self):

        participant_team_data = json.loads(
            challenge_response.challenge_participant_teams
        )

        url = "{}{}"

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_teams.value),
            json=participant_team_data,
            status=200,
        )
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_challenges.value).format(
                "3"
            ),
            status=404,
        )

        self.expected = "404 Client Error: Not Found for url: {}"

    @responses.activate
    def test_get_participant_or_host_team_challenges_for_http_error_404(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant"])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.participant_challenges.value)
        assert response == self.expected.format(url.format("3"))


class TestGetParticipantOrHostTeamChallengesRequestForExceptions(
    BaseTestClass
):
    def setup(self):

        participant_team_data = json.loads(
            challenge_response.challenge_participant_teams
        )

        url = "{}{}"

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_teams.value),
            json=participant_team_data,
            status=200,
        )
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_challenges.value).format(
                "3"
            ),
            body=Exception("..."),
        )

        self.expected = "404 Client Error: Not Found for url: {}"

    @responses.activate
    def test_get_participant_or_host_team_challenges_for_request_exception(
        self
    ):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant"])
        assert result.exit_code == -1


class TestRequestForExceptions(BaseTestClass):
    def setup(self):

        url = "{}{}"

        # Challenge URLS

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.create_challenge.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.past_challenge_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.future_challenge_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_teams.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.host_teams.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_challenges.value).format(
                "3"
            ),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.host_challenges.value).format("2"),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_details.value.format("1")),
            body=RequestException("..."),
        )

        # Teams URLS

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            body=RequestException("..."),
        )

        responses.add(
            responses.POST,
            url.format(
                API_HOST_URL, URLS.participate_in_a_challenge.value
            ).format("2", "3"),
            body=RequestException("..."),
        )

        # Phase URLS

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_list.value).format(
                "10"
            ),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "10", "20"
            ),
            body=RequestException("..."),
        )

        # Submission URLS
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.my_submissions.value).format(
                "3", "7"
            ),
            body=RequestException("..."),
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
            body=RequestException("..."),
        )

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            body=RequestException("..."),
        )

        # Phase Split URLS
        responses.add(
            responses.GET,
            url.format(
                API_HOST_URL, URLS.challenge_phase_split_detail.value
            ).format("1"),
            body=RequestException("..."),
        )

        # Leaderboard URLS
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.leaderboard.value).format("1"),
            body=RequestException("..."),
        )

    @responses.activate
    def test_create_challenge_for_request_exception(self):
        runner = CliRunner()
        my_path = os.path.abspath(os.path.dirname(__file__))
        file = os.path.join(my_path, "data")
        result = runner.invoke(challenges, ["create", "--file", "{}/test_zip_file.zip".format(file), "4"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_challenge_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges)
        assert result.exit_code == 1

    @responses.activate
    def test_display_past_challenge_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["past"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_ongoing_challenge_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["ongoing"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_future_challenge_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["future"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_host_challenge_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--host"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_participant_challenge_lists_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_participant_and_host_challenge_lists_for_request_exception(
        self
    ):
        runner = CliRunner()
        result = runner.invoke(challenges, ["--participant", "--host"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_participant_team_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(teams, ["--participant"])
        assert result.exit_code == 1

    @responses.activate
    def test_create_team_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(
            teams, ["create", "participant"], input="TeamTest\ny\nN"
        )
        assert result.exit_code == 1

    @responses.activate
    def test_participate_in_a_challenge_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "participate", "3"], input="Y")
        assert result.exit_code == 1

    @responses.activate
    def test_display_challenge_phase_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phases"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_challenge_phase_detail_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["10", "phase", "20"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_my_submission_details_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["3", "phase", "7", "submissions"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_submission_details_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(submission, ["9"])
        assert result.exit_code == 1

    @responses.activate
    def test_make_submission_for_request_exception(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="N",
            )
            assert result.exit_code == 1

    @responses.activate
    def test_display_challenge_phase_split_list_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["1", "phase", "2", "splits"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_leaderboard_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["2", "leaderboard", "1"])
        assert result.exit_code == 1

    @responses.activate
    def test_display_challenge_details_for_request_exception(self):
        runner = CliRunner()
        result = runner.invoke(challenge, ["1"])
        assert result.exit_code == 1


class TestTeamsSuccess(BaseTestClass):
    def setup(self):
        url = "{}{}"

        self.challenge_id = "2"
        self.team_id = "3"
        self.team_name = "TeamTest"
        self.expected_partic_team = "\nYour participant team {} was successfully created.\n".format(self.team_name)
        self.expected_host_team = "\nYour host team {} was successfully created.\n".format(self.team_name)
        self.expected_participate = "Your team id {} is now participating in this challenge.\n".format(self.team_id)

        headers = get_request_header()
        headers["Content-Type"] = "application/json"

        data = {}
        data["team_name"] = self.team_name
        data = json.loads(json.dumps(data))

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participant_team_list.value),
            headers=headers,
            json=data,
            status=201)

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.create_host_team.value),
            headers=headers,
            json=data,
            status=201)

        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.participate_in_a_challenge.value).format(self.challenge_id, self.team_id),
            status=201)

    @responses.activate
    def test_create_participant_team_success(self):
        user_prompt_text = (
            "Enter team name: {tn}\n"
            "Please confirm the team name - {tn} [y/N]: y\n"
            "Do you want to enter the Team URL [y/N]: N\n"
        ).format(tn=self.team_name)

        runner = CliRunner()
        result = runner.invoke(teams, ["create", "participant"], input="TeamTest\ny\nN")
        response = result.output
        expected = self.expected_partic_team
        expected = "{}{}\n".format(user_prompt_text, expected)
        assert response == expected

    @responses.activate
    def test_create_host_team_success(self):
        user_prompt_text = (
            "Enter team name: TeamTest\n"
            "Please confirm the team name - TeamTest [y/N]: y\n"
            "Do you want to enter the Team URL [y/N]: N\n"
        )

        runner = CliRunner()
        result = runner.invoke(teams, ["create", "host"], input="TeamTest\ny\nN")
        response = result.output
        expected = self.expected_host_team
        expected = "{}{}\n".format(user_prompt_text, expected)
        assert response == expected

    @responses.activate
    def test_participate_in_a_challenge_success(self):
        terms_and_conditions_page_url = "{}{}".format(get_host_url(), URLS.terms_and_conditions_page.value)
        terms_and_conditions_page_url = terms_and_conditions_page_url.format(self.challenge_id)
        expected = (
            "Please refer challenge terms and conditions here: {}"
            "\n\nBy agreeing to participate in the challenge, you are agreeing to terms and conditions."
            "\n\nDo you accept challenge terms and conditions? [y/N]: Y\n".format(terms_and_conditions_page_url)
            + self.expected_participate
        )

        runner = CliRunner()
        result = runner.invoke(challenge, [self.challenge_id, "participate", self.team_id], input="Y")
        response = result.output
        assert response == expected

    @responses.activate
    def test_participate_in_a_challenge_decline_terms_and_conditions(self):
        terms_and_conditions_page_url = "{}{}".format(get_host_url(), URLS.terms_and_conditions_page.value)
        terms_and_conditions_page_url = terms_and_conditions_page_url.format(self.challenge_id)
        expected = (
            "Please refer challenge terms and conditions here: {}"
            "\n\nBy agreeing to participate in the challenge, you are agreeing to terms and conditions."
            "\n\nDo you accept challenge terms and conditions? [y/N]: N".format(terms_and_conditions_page_url)
            + "\n\nYou can't participate in the challenge without accepting terms and conditions\n"
        )

        runner = CliRunner()
        result = runner.invoke(challenge, [self.challenge_id, "participate", self.team_id], input="N")
        response = result.output
        assert response == expected
