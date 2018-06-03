import json
import responses

from click.testing import CliRunner

from evalai.teams import teams
from tests.data import teams_response

from evalai.utils.challenges import API_HOST_URL
from evalai.utils.urls import Urls

class TestTeams:
    def setup(self):
        team_list_data = json.loads(teams_response.teams_list)
        team_created_data = json.loads(teams_response.create_team)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, Urls.participant_team_lists.value),
                      json=team_list_data, status=200)

        responses.add(responses.POST, url.format(API_HOST_URL, Urls.participant_team_lists.value),
                      json=team_created_data, status=201)

        responses.add(responses.POST, url.format(API_HOST_URL, Urls.challenge_participate.value).format("2", "3"),
                      json=team_list_data, status=201)

        self.teams = team_list_data["results"]

    @responses.activate
    def test_teams_list(self):

        output = ""
        for team in self.teams:
            br = ("----------------------------------------"
                  "--------------------------")

            team_name = "\n{}".format(team["team_name"],)
            team_id = "ID: {}\n\n".format(str(team["id"]),)
            title = "{} {}".format(team_name, team_id)
            created_by = "Created by : {}\n\n".format(team["created_by"])
            members = "{}\n".format("Members")
            for member in team["members"]:
                members = "{}* {}\n".format(members, member["member_name"])
            team = "{}{}{}\n{}\n".format(title, created_by, members, br)

            output = output + team

        runner = CliRunner()
        result = runner.invoke(teams, ['list'])
        response_table = result.output
        assert response_table == output

    @responses.activate
    def test_create_team_option_yes(self):
        output = ("Enter team name: : TeamTest\n"
                  "Please confirm the team name - TeamTest [y/N]: y\n"
                  "\nThe team TestTeam was successfully created.\n\n")
        runner = CliRunner()
        result = runner.invoke(teams, ['create'], input="TeamTest\ny\n")
        response_table = result.output
        assert response_table == output

    @responses.activate
    def test_create_team_option_no(self):
        output = ("Enter team name: : TeamTest\n"
                  "Please confirm the team name - TeamTest [y/N]: n\n"
                  "Aborted!\n")
        runner = CliRunner()
        result = runner.invoke(teams, ['create'], input="TeamTest\nn\n")
        response_table = result.output
        assert response_table == output

    @responses.activate
    def test_participate(self):
        output = "Your participant team is now participating in this challenge.\n"
        runner = CliRunner()
        result = runner.invoke(teams, ['participate', '-c', '2', '-pt', '3'])
        response_table = result.output
        assert response_table == output

    @responses.activate
    def test_participate_single_argument(self):
        output = ("Usage: teams participate [OPTIONS]\n"
                  "\nError: Missing option \"-pt\" / \"--participant-team\".\n"
                 )
        runner = CliRunner()
        result = runner.invoke(teams, ['participate', '-c', '2'])
        response_table = result.output
        assert response_table == output

    @responses.activate
    def test_participate_string_argument(self):
        output = (
                  "Usage: teams participate [OPTIONS]\n"
                  "\nError: Invalid value for \"-c\" / \"--challenge-id\": two is not a valid integer\n"
                 )
        runner = CliRunner()
        result = runner.invoke(teams, ['participate', '-c', 'two', '-pt', '3'])
        response_table = result.output
        assert response_table == output
