from click import echo

def valid_token(response):
    """
    Checks if token is valid.
    """
    if ('detail' in response) and (response['detail'] == 'Invalid token'):
        return False
    return True
