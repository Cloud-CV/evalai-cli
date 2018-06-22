import responses

from click.testing import CliRunner

from evalai.challenges import challenges
from evalai.utils.urls import URLS
from evalai.utils.config import API_HOST_URL

from .base import BaseTestClass


class TestRequests(BaseTestClass):

    def setup(self):

        url = "{}{}"
        responses.add(responses.GET, url.format(API_HOST_URL, URLS.challenge_list.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.past_challenge_list.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.challenge_list.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.future_challenge_list.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.participant_teams.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.host_teams.value), status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.participant_challenges.value).format("3"),
                      status=404)

        responses.add(responses.GET, url.format(API_HOST_URL, URLS.host_challenges.value).format("2"), status=404)

        self.expected = "404 Client Error: Not Found for url: {}"

    @responses.activate
    def test_404_challenge_list(self):
        runner = CliRunner()
        result = runner.invoke(challenges)
        response_table = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
        assert response_table == self.expected.format(url)

    @responses.activate
    def test_404_past_challenge_list(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['past'])
        response_table = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.past_challenge_list.value)
        assert response_table == self.expected.format(url)

    @responses.activate
    def test_404_ongoing_challenge_list(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['ongoing'])
        response_table = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.challenge_list.value)
        assert response_table == self.expected.format(url)

    @responses.activate
    def test_404_future_challenge_list(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['future'])
        response_table = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.future_challenge_list.value)
        assert response_table == self.expected.format(url)

    @responses.activate
    def test_404_host_challenge_list(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['--host'])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.host_teams.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_404_participant_challenge_lists(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['--participant'])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.participant_teams.value)
        assert response == self.expected.format(url)

    @responses.activate
    def test_404_participant_and_host_challenge_lists(self):
        runner = CliRunner()
        result = runner.invoke(challenges, ['--participant', '--host'])
        response = result.output.rstrip()
        url = "{}{}".format(API_HOST_URL, URLS.host_teams.value)
        assert response == self.expected.format(url)
