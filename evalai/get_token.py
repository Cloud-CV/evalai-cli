import click
import os

from click import echo, style

from evalai.utils.config import AUTH_TOKEN_PATH
import json
from json.decoder import JSONDecodeError


@click.group(invoke_without_command=True)
def get_token():
    """
    Get the EvalAI token.
    """
    if not os.path.exists(AUTH_TOKEN_PATH):
        echo(
            style(
                "\nThe authentication token json file doesn't exist at the required path. "
                "Please download the file from the Profile section of the EvalAI webapp and "
                "place it at ~/.evalai/token.json or use evalai -t <token> to add it.\n\n",
                bold=True,
                fg="red",
            )
        )
    else:
        with open(AUTH_TOKEN_PATH, "r") as fr:
            try:
                data = fr.read()
                tokendata = json.loads(data)
                echo("Current token is {}".format(tokendata["token"]))
            except (OSError, IOError) as e:
                echo(str(e))
            except JSONDecodeError as e:
                msg = "Decode Error: " + str(e) +" \n The 'token.json' file was empty"
                echo(msg)
            except KeyError as e:
                echo("The following key was not found in 'token.json': " + str(e))
