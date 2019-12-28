import json
import os
import random
import shutil
import string
import tempfile

from io import StringIO
from unittest import mock
from unittest import TestCase

from evalai.utils.auth import reset_user_auth_token


class TestResetUserAuthToken(TestCase):
    def setUp(self):
        self.base_temp_dir = tempfile.mkdtemp()
        self.token_dir = os.path.join(self.base_temp_dir, ".evalai")
        self.token_path = os.path.join(self.token_dir, "token.json")

        self.token = "".join(random.choice(string.ascii_lowercase) for _ in range(40))
        self.token_json = json.dumps({"token": self.token})

        os.makedirs(self.token_dir)
        with open(self.token_path, "w") as fw:
            fw.write(self.token_json)

        self.patcher = mock.patch("evalai.utils.auth.AUTH_TOKEN_PATH", self.token_path)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.base_temp_dir):
            shutil.rmtree(self.base_temp_dir)

    def test_reset_user_auth_token_success(self):
        self.assertTrue(os.path.exists(self.token_path))  # Make sure the path exists already
        reset_user_auth_token()

        self.assertFalse(os.path.exists(self.token_path))

    def test_reset_user_auth_token_when_token_is_not_configured(self):
        os.remove(self.token_path)
        expected = """The authentication token has not been configured. Please use the commands 
                   `evalai login` or `evalai set_token TOKEN` first to set up the configuration."""

        with mock.patch("sys.stdout", StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                reset_user_auth_token()
            exit_code = cm.exception.code
            value = fake_out.getvalue().strip()

        self.assertEqual(exit_code, 1)
        self.assertEqual(value, expected)

    @mock.patch("evalai.utils.auth.os.remove")
    def test_reset_user_auth_token_when_writing_to_file_fails(self, mock_remove):
        error = "ExampleError: Example Error Description"
        mock_remove.side_effect = OSError(error)

        with mock.patch("sys.stdout", StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                reset_user_auth_token()
            exit_code = cm.exception.code
            value = fake_out.getvalue().strip()

        self.assertEqual(exit_code, 1)
        self.assertEqual(value, error)
