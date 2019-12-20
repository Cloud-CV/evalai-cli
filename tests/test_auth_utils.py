import mock
import os
import logging
import shutil

from io import StringIO
from unittest import TestCase

from evalai.utils.auth import write_host_url_to_file


class TestAuthUtilsBaseClass(TestCase):
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


class TestWriteHostUrlToFile(TestAuthUtilsBaseClass):
    def setUp(self):
        super(TestWriteHostUrlToFile, self).setUp()
        self.new_host = "http://testserver.abc"
        self.temp_host_path = os.path.join(self.fake_token_dir, "host_url")
        self.host_path_patcher = mock.patch("evalai.utils.auth.HOST_URL_FILE_PATH", self.temp_host_path)
        self.host_path_patcher.start()

    def tearDown(self):
        super(TestWriteHostUrlToFile, self).tearDown()
        self.host_path_patcher.stop()

    def test_write_host_url_to_file_success(self):
        fake_open = mock.mock_open()
        patcher = mock.patch("evalai.utils.auth.open", fake_open)
        patcher.start()
        handler = fake_open()
        expected = "{} is set as the host url.\n".format(self.new_host)
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            write_host_url_to_file(self.new_host)
            fake_open.assert_called_with(self.temp_host_path, "w")
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)
        patcher.stop()

    def test_write_host_url_to_file_fail(self):
        fake_open = mock.mock_open()
        patcher = mock.patch("evalai.utils.auth.open", fake_open)
        patcher.start()
        handler = fake_open()
        handler.write.side_effect = OSError("Permission denied.")
        expected = "Permission denied.\n"
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                write_host_url_to_file(self.new_host)
                self.assertEqual(cm.exception.error_code, 1)
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)
        patcher.stop()
