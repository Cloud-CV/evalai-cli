import ast
import click
import json
import responses
import subprocess

from click.testing import CliRunner
from click import echo, style
from pylsy import pylsytable

from evalai.challenges import challenges
from tests.data import challenge_response

from evalai.utils.challenges import API_HOST_URL
from evalai.utils.urls import Urls


class TestChallenges:

    def setup(self):

        json_data = ast.literal_eval(challenge_response.challenges)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, Urls.challenge_list.value),
                      json=json_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.past_challenge_list.value),
                      json=json_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.challenge_list.value),
                      json=json_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.future_challenge_list.value),
                      json=json_data, status=200)

        challenges = json_data["results"]

        self.output = ""

        title = "\n{}".format("{}")
        idfield = "{}\n\n".format("{}")
        subtitle = "\n{}\n\n".format("{}")
        br = "------------------------------------------------------------------\n"

        for challenge in challenges:
            challenge_title = title.format(challenge["title"])
            challenge_id = "ID: " + idfield.format(challenge["id"])

            heading = "{} {}".format(challenge_title, challenge_id)
            description = "{}\n".format(challenge["short_description"])
            date = "End Date : " + challenge["end_date"].split("T")[0]
            date = subtitle.format(date)
            challenge = "{}{}{}{}".format(heading, description, date, br)

            self.output = self.output + challenge


    @responses.activate
    def test_challenge_lists(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list'])
        response_table = result.output
        assert response_table == self.output


    @responses.activate
    def test_challenge_lists_past(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'past'])
        response_table = result.output
        assert response_table == self.output

    @responses.activate
    def test_challenge_lists_ongoing(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'ongoing'])
        response_table = result.output
        assert response_table == self.output

    @responses.activate
    def test_challenge_lists_future(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'future'])
        response_table = result.output
        assert response_table == self.output


class TestTeamChallenges:

    def setup(self):

        challenge_data = ast.literal_eval(challenge_response.challenges)
        host_team_data = ast.literal_eval(challenge_response.challenge_host_teams)
        participant_team_data = ast.literal_eval(challenge_response.challenge_participant_teams)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, Urls.participant_teams.value),
                      json=participant_team_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.host_teams.value),
                      json=host_team_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.participant_challenges.value).format("3"),
                      json=challenge_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.host_challenges.value).format("2"),
                      json=challenge_data, status=200)

        challenges = challenge_data["results"]

        self.output = ""

        title = "\n{}".format("{}")
        idfield = "{}\n\n".format("{}")
        subtitle = "\n{}\n\n".format("{}")
        br = "------------------------------------------------------------------\n"

        for challenge in challenges:
            challenge_title = title.format(challenge["title"])
            challenge_id = "ID: " + idfield.format(challenge["id"])

            heading = "{} {}".format(challenge_title, challenge_id)
            description = "{}\n".format(challenge["short_description"])
            date = "End Date : " + challenge["end_date"].split("T")[0]
            date = subtitle.format(date)
            challenge = "{}{}{}{}".format(heading, description, date, br)

            self.output = self.output + challenge

    @responses.activate
    def test_challenge_lists_host(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', '--host'])
        response_table = result.output
        assert response_table == self.output

    @responses.activate
    def test_challenge_lists_participant(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', '--participant'])
        response_table = result.output
        assert response_table == self.output


class TestChallengePhases:

    def setup(self):
        challenge_phase_list_json = json.loads(challenge_response.challenge_phase_list)
        challenge_phase_details_json = json.loads(challenge_response.challenge_phase_details)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, Urls.phase_list.value).format('10'),
                      json=challenge_phase_list_json, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, Urls.phase_details.value).format('10', '20'),
                      json=challenge_phase_details_json, status=200)
        self.phases = challenge_phase_list_json['results']
        self.phase = challenge_phase_details_json

    @responses.activate
    def test_challenge_phase_lists(self):

        self.output = ""

        for phase in self.phases:
            br = ("--------------------------------"
                  "----------------------------------")

            phase_title = "\n{}".format(phase["name"])
            challenge_id = "Challenge ID: {}".format(str(phase["challenge"]))
            phase_id = "Phase ID: {}\n\n".format(str(phase["id"]))

            title = "{} {} {}".format(phase_title, challenge_id, phase_id)

            description = "{}\n\n".format(phase["description"])
            phase = "{}{}{}\n".format(title, description, br)

            self.output = self.output + phase

        runner = CliRunner()
        result = runner.invoke(challenges, ['phases', 'list', '-c', '10'])
        response_table = result.output
        assert response_table == self.output

    @responses.activate
    def test_challenge_phase_details(self):

        phase = self.phase
        phase_title = "\n{}".format(phase["name"])
        challenge_id = "Challenge ID: {}".format(str(phase["challenge"]))
        phase_id = "Phase ID: {}\n\n".format(str(phase["id"]))

        title = "{} {} {}".format(phase_title, challenge_id, phase_id)

        description = "{}\n".format(phase["description"])

        start_date = "Start Date : " + phase["start_date"].split("T")[0]
        start_date = "\n{}\n".format(start_date)

        end_date = "End Date : " + phase["end_date"].split("T")[0]
        end_date = "\n{}\n".format(end_date)

        max_submissions_per_day = "\nMaximum Submissions per day : {}\n".format(
                                    str(phase["max_submissions_per_day"]))

        max_submissions = "\nMaximum Submissions : {}\n".format(
                                    str(phase["max_submissions"]))

        codename = "\nCode Name : {}\n".format(
                                              phase["codename"])

        leaderboard_public = "\nLeaderboard Public : {}\n".format(
                                              phase["leaderboard_public"])

        is_active = "\nActive : {}\n".format(phase["is_active"])

        is_public = "\nPublic : {}\n".format(phase["is_public"])

        phase = "{}{}{}{}{}{}{}{}{}{}\n".format(title, description, start_date, end_date,
                                              max_submissions_per_day, max_submissions, leaderboard_public,
                                              codename, is_active, is_public)

        runner = CliRunner()
        result = runner.invoke(challenges, ['phases', '-c', '10', '-p', '20'])
        response_table = result.output
        assert response_table == phase
