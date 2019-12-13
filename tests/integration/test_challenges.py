import requests

from unittest import TestCase

from evalai.utils.config import API_HOST_URL
from evalai.utils.urls import URLS


class BaseTestClass(TestCase):
    def setUp(self):
        self.url = "{}{}"
        self.host_url = API_HOST_URL

    def test_challenges_when_token_is_missing(self):
        response = requests.get(
            self.url.format(self.host_url, URLS.challenge_list.value)
        )
        expected = "Sorry, no challenges found."
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)
