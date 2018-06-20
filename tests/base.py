import json
import os
import random
import string

import os.path as osp

from evalai.utils.config import AUTH_TOKEN_PATH

random.seed(10)


class BaseTestClass:

    @classmethod
    def setup_class(cls):
        if not os.path.exists(AUTH_TOKEN_PATH):
            os.makedirs(AUTH_TOKEN_PATH)
            with open(osp.join(AUTH_TOKEN_PATH, FILE), 'w') as fw:
                token = ''.join(random.choice(string.ascii_lowercase) for _ in range(40))
                data = {"token": "{}".format(token)}
                fw.write(json.dumps(data))
