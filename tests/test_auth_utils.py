import json
import logging
import mock
import os
import random
import shutil
import string

from io import StringIO
from unittest import TestCase

from evalai.utils.auth import write_host_url_to_file

random.seed(42)


class AuthUtilsTestBaseClass(TestCase):
    def setUp(self):
        self.base_temp_dir = "temp-dir/"
        if not os.path.exists(self.base_temp_dir):
            os.makedirs(self.base_temp_dir)

        # Important to mock out the config files
        # as any unintended changes in these may
        # cause other tests to fail.
        self.fake_token_dir = os.path.join(self.base_temp_dir, "evalai")
        self.token_dir_patcher = mock.patch("evalai.utils.auth.AUTH_TOKEN_DIR", self.fake_token_dir)
        self.token_dir_patcher.start()

    def tearDown(self):
        self.token_dir_patcher.stop()
        try:
            shutil.rmtree(self.base_temp_dir)
        except:
            logging.critical("Unable to delete temporary directory: {}".format(self.base_temp_dir))


class TestWriteHostUrlToFile(AuthUtilsTestBaseClass):
    def setUp(self):
        super(TestWriteHostUrlToFile, self).setUp()
        self.new_host = "http://testserver.abc"
        self.temp_host_path = os.path.join(self.fake_token_dir, "host_url")
        self.host_path_patcher = mock.patch("evalai.utils.auth.HOST_URL_FILE_PATH", self.temp_host_path)
        self.host_path_patcher.start()

        self.fake_open = mock.mock_open()
        self.file_open_patcher = mock.patch("evalai.utils.auth.open", self.fake_open)
        self.file_open_patcher.start()

    def tearDown(self):
        self.fake_open.reset_mock(side_effect=True)
        self.file_open_patcher.stop()
        self.host_path_patcher.stop()
        super(TestWriteHostUrlToFile, self).tearDown()

    def test_write_host_url_to_file_success(self):
        handler = self.fake_open()
        expected = "{} is set as the host url.\n".format(self.new_host)
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            write_host_url_to_file(self.new_host)
            self.fake_open.assert_called_with(self.temp_host_path, "w")
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)

    def test_write_host_url_to_file_fail(self):
        handler = self.fake_open()
        handler.write.side_effect = OSError("Permission denied.")  # For example
        expected = "Permission denied.\n"
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                write_host_url_to_file(self.new_host)
                self.assertEqual(cm.exception.error_code, 1)
            self.fake_open.assert_called_with(self.temp_host_path, "w")
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)


class TestWriteAuthTokenToFile(AuthUtilsTestBaseClass):
    def setUp(self):
        super(TestWriteAuthTokenToFile, self).setUp()
        self.token = "".join(
            random.choice(string.ascii_lowercase) for _ in range(40)
        )
        self.token_json = json.dumps({"token": self.token})
        self.expected = json.dumps(self.token_json)
        self.temp_token_path = os.path.join(self.fake_token_dir, "token.json")
        self.token_path_patcher = mock.patch(
            "evalai.utils.auth.AUTH_TOKEN_PATH", self.temp_token_path
        )
        self.token_path_patcher.start()

    def tearDown(self):
        self.token_path_patcher.stop()
        super(TestWriteAuthTokenToFile, self).tearDown()

    def test_write_token_json_to_file_success(self):
        write_json_auth_token_to_file(self.token_json)
        with open(self.temp_token_path, "r") as tokenfile:
            self.assertEqual(tokenfile.read(), self.expected)

    @mock.patch("evalai.utils.auth.json.dump")
    def test_write_token_json_to_file_fail(self, mock_json):
        error_description = "Example Error Descripton"
        expected = "{}\n".format(error_description)
        mock_json.side_effect = OSError(error_description)
        with mock.patch('sys.stdout', StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                write_json_auth_token_to_file(self.token_json)
                self.assertEqual(cm.exception.error_code, 1)
            self.assertEqual(fake_out.getvalue(), expected)

    def test_write_token_to_file_success(self):
        write_auth_token_to_file(self.token)
        with open(self.temp_token_path, "r") as tokenfile:
            self.assertEqual(tokenfile.read(), self.expected)
