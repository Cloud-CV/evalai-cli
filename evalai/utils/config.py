# Store all the varibales here
import os

from os.path import expanduser


LEN_OF_TOKEN = 210

AUTH_TOKEN_FILE_NAME = "token.json"

HOST_URL_FILE_NAME = "host_url"

AUTH_TOKEN_DIR = expanduser("~/.evalai/")

AUTH_TOKEN_PATH = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

API_HOST_URL = os.environ.get("EVALAI_API_URL", "https://eval.ai")

EVALAI_ERROR_CODES = [400, 401, 403, 406]

HOST_URL_FILE_PATH = os.path.join(AUTH_TOKEN_DIR, HOST_URL_FILE_NAME)

EVALAI_HOST_URLS = [
    "https://eval.ai",
    "https://staging.eval.ai",
    "http://localhost:8888",
]

ENVIRONMENT = os.environ.get("EVALAI_CLI_ENVIRONMENT", "PRODUCTION")

LOCAL_DOCKER_REGISTRY_URI = os.environ.get(
    "EVALAI_LOCAL_DOCKER_REGISTRY_URI", "localhost:5000"
)

AWS_REGION = os.environ.get("AWS_REGION_NAME", "us-east-1")
