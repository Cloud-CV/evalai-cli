import click
import subprocess

from evalai.utils.config import STARTER_URL


@click.group(invoke_without_command=True)
def get_starter():
    """
    Download the EvalAI-Starter
    """
    download_path = click.prompt("Enter directory to store EvalAI-Starters in", type=str, hide_input=False)
    subprocess.run(["git", "clone", STARTER_URL, download_path])
