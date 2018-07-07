from os.path import expanduser


AUTH_TOKEN_FILE = 'token.json'

HOST_URL_FILE = 'host_url'

EVALAI_FILE_PATH = "{}/.evalai/".format(expanduser('~'))

AUTH_TOKEN_FILE_PATH = "{}{}".format(EVALAI_FILE_PATH, AUTH_TOKEN_FILE)

HOST_URL_FILE_PATH = "{}{}".format(EVALAI_FILE_PATH, HOST_URL_FILE)
