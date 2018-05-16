import ast
import click
import responses

from click.testing import CliRunner
from pylsy import pylsytable

from evalai.challenges import challenges
from tests.data import challenge_response

from evalai.utils.challenges import API_HOST_URL
from evalai.utils.urls import urls


class TestChallenges:

    def setup(self):

        json_data = ast.literal_eval(challenge_response.challenges)

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, urls["get_challenge_list"]),
                      json=json_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, urls["get_past_challenge_list"]),
                      json=json_data, status=200)

        responses.add(responses.GET, url.format(API_HOST_URL, urls["get_future_challenge_list"]),
                      json=json_data, status=200)

        column_names = ['ID', 'Challenge Name']
        attributes = ['id', 'title']
        table = pylsytable(column_names)

        challenges_response = json_data["results"]
        for attribute, column_name in zip(attributes, column_names):
            items = []
            for challenge in challenges_response:
                items.append(challenge[attribute])

            table.add_data(column_name, items)

        self.CLI_table = str(table).rstrip()

    @responses.activate
    def test_challenge_lists(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table

    @responses.activate
    def test_challenge_lists_past(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'past'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table

    @responses.activate
    def test_challenge_lists_future(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['list', 'future'])
        response_table = result.output.rstrip()
        assert response_table == self.CLI_table
