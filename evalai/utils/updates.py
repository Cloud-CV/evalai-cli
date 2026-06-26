import requests

from packaging.version import Version as StrictVersion


def get_latest_version():
    url = "https://pypi.org/pypi/evalai/json"
    response = requests.get(url)
    data = response.json()
    versions = list(data["releases"].keys())
    versions.sort(key=StrictVersion)
    return versions[-1]
