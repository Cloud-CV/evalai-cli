import click
import sys
import os

from click import echo, style

from evalai.utils.config import STDOUT_FILE_PATH
import json


@click.group(invoke_without_command=True)
def display():
    """
    Display stdout file.
    """
    if not os.path.exists(STDOUT_FILE_PATH):
        echo(
            style(
                "\nThe stdout file doesn't exist at the required path. "
                "Please create it at ~/.evalai/stdout.txt or use cat ~/.evalai/stdout.txt to add it.\n\n",
                bold=True,
                fg="red",
            )
        )
    else:
        with open(STDOUT_FILE_PATH, "r") as fr:
            try:
                file_contents = fr.read()
                print (file_contents)
                fr.close()
                # data = fr.read()
                # tokendata = json.loads(data)
                # echo("Current token is {}".format(tokendata["token"]))
            except (OSError, IOError) as e:
                echo(e)
