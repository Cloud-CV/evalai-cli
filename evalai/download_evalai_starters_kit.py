import click
import subprocess

from evalai.utils.config import STARTERS_URL


@click.group(invoke_without_command=True)
def download_evalai_starters_kit():
    """
    Download the EvalAI-Starters kit.
    """
    download_path = click.prompt("Enter directory to store EvalAI-Starters in", type=str, hide_input=False)
    subprocess.run(["git", "clone", STARTERS_URL, download_path])
