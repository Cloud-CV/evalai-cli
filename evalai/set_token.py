import click
import os
from evalai.utils.config import AUTH_TOKEN_DIR
@click.group(invoke_without_command=True)
@click.argument('TOKEN')
def token(token):
    """
    Add or change your token.
    """
    """
    Invoked by `evalai token TOKEN`.
    """
    input_token = token
    if not os.path.exists(AUTH_TOKEN_DIR):
        os.makedirs(AUTH_TOKEN_DIR)
    AUTH_TOKEN_PATH_NEW = "%stoken.json" % AUTH_TOKEN_DIR
    f=open(AUTH_TOKEN_PATH_NEW,"w+") 
    json_token = "{\"token\":\"%s\"}" % input_token
    f.write(json_token)
    f.close()
    print("Token successfully set!")
    return input_token

# flake8: noqa
