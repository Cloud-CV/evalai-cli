import requests

from click.testing import CliRunner
from unittest import TestCase

from evalai.add_token import set_token
from evalai.challenges import challenges, challenge

from evalai.utils.config import API_HOST_URL
from evalai.utils.urls import URLS


class BaseTestClass(TestCase):
    def setUp(self):
        self.url = "{}{}"
        self.host_url = API_HOST_URL

    def set_token_to_undefined(self):
        runner = CliRunner()
        runner.invoke(set_token, "0"*40)

    def test_challenges_when_token_is_missing(self):
        self.set_token_to_undefined()
        runner = CliRunner()
        expected = "The authentication token you are using isn't valid. Please generate it again."
        result = runner.invoke(challenges)
        assert expected == result.rstrip()
