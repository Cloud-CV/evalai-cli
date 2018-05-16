from click import echo


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Text:
    title = "\n{0}{1}{3}{2}".format(Colors.BOLD, Colors.OKGREEN, Colors.ENDC, "{}")
    idfield = "{0}{1}{3}{2}\n".format(Colors.BOLD, Colors.OKBLUE, Colors.ENDC, "{}")
    subtitle = "\n{0}{2}{1}\n".format(Colors.BOLD, Colors.ENDC, "{}")
    br = "{0}------------------------------------------------------------------".format(Colors.BOLD)


def valid_token(response):
    """
    Checks if token is valid.
    """

    if ('detail' in response):
        if (response['detail'] == 'Invalid token'):
            echo("The authentication token you are using isn't valid. Please try again.")
            return False
        if (response['detail'] == 'Token has expired'):
            echo("Sorry, the token has expired.")
            return False
    return True
