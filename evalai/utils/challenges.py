import os
import json
import requests

from click import echo

from pylsy import pylsytable

from evalai.utils.auth import get_headers
from evalai.utils.urls import urls
from evalai.utils.common import valid_token


API_HOST_URL = os.environ.get("EVALAI_API_URL", 'http://localhost:8000')


def get_challenges(url):

    headers = get_headers()
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    if valid_token(response_json):

        column_names = ['ID', 'Challenge Name', 'Short Description']
        attributes = ['id', 'title', 'short_description']
        table = pylsytable(column_names)

        challenges = response_json["results"]
        for attribute, column_name in zip(attributes, column_names):
            items = []
            for challenge in challenges:
                if attribute == 'short_description':
                    items.append(challenge[attribute][:50])
                else:
                    items.append(challenge[attribute])

            table.add_data(column_name, items)
        echo(table)
    else:
        echo("The authentication token you are using isn't valid. Please try again")



def get_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_challenge_list"])
    get_challenges(url)


def get_past_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_past_challenge_list"])
    get_challenges(url)


def get_future_challenge_list():
    """
    Fetches the list of challenges from the backend.
    """
    url = "{}{}".format(API_HOST_URL, urls["get_future_challenge_list"])
    get_challenges(url)
