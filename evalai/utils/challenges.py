import json
import requests

from click import echo

from pylsy import pylsytable

from evalai.utils.auth import get_headers
from evalai.utils.urls import urls


DOMAIN = "http://localhost:8000"


def get_challenges(url):

    headers = get_headers()

    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)

    column_names = ['ID', 'Challenge Name']
    attributes = ['id', 'title']
    table = pylsytable(column_names)

    challenges = response_json["results"]
    for attribute, column_name in zip(attributes, column_names):
        items = []
        for challenge in challenges:
            items.append(challenge[attribute])
        table.add_data(column_name, items)
    echo(table)


def get_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(DOMAIN, urls["get_challenge_list"])
    get_challenges(url)


def get_past_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(DOMAIN, urls["get_past_challenge_list"])
    get_challenges(url)


def get_future_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(DOMAIN, urls["get_future_challenge_list"])
    get_challenges(url)
