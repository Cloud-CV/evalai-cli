import json
import os
import random
import string

import os.path as osp

from evalai.utils.config import AUTH_TOKEN_FILE_NAME, AUTH_TOKEN_DIR

random.seed(10)


class BaseTestClass:

    @classmethod
    def setup_class(cls):
        token_file = osp.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)
        if not os.path.exists(token_file):
            os.makedirs(AUTH_TOKEN_DIR)
            with open(token_file, 'w') as fw:
                token = ''.join(random.choice(string.ascii_lowercase) for _ in range(40))
                data = {"token": "{}".format(token)}
                fw.write(json.dumps(data))
