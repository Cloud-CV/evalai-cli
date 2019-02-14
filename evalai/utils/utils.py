def convert_bytes_to(byte, to, bsize=1024):
    """
    Convert bytes to KB, MB, GB etc.
    
    Arguments:
        bytes {int} -- The bytes which is to be converted
        to {str} -- To which unit it is to be converted
    """
    units_mapping = {
        'k': 1,
        'm': 2,
        'g': 3,
        't': 4,
        'p': 5,
        'e': 6
    }
    for value in range(units_mapping[to]):
        byte  = int(byte / bsize)
    
    return byte
