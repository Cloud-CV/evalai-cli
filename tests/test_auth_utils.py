import mock

from io import StringIO
from unittest import TestCase

from evalai.utils.auth import write_host_url_to_file
from evalai.utils.config import HOST_URL_FILE_PATH


class TestWriteHostUrlToFile(TestCase):
    def setUp(self):
        self.new_host = "http://testserver.abc"

    def test_write_host_url_to_file_success(self):
        fake_open = mock.mock_open()
        patcher = mock.patch("evalai.utils.auth.open", fake_open)
        patcher.start()
        handler = fake_open()
        expected = "{} is set as the host url.\n".format(self.new_host)
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            write_host_url_to_file(self.new_host)
            fake_open.assert_called_with(HOST_URL_FILE_PATH, "w")
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)
        patcher.stop()

    def test_write_host_url_to_file_fail(self):
        fake_open = mock.mock_open()
        patcher = mock.patch("evalai.utils.auth.open", fake_open)
        patcher.start()
        handler = fake_open()
        handler.write.side_effect = OSError("Permission denied.")
        expected = "Permission denied.\nNone\n"
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                write_host_url_to_file(self.new_host)
                self.assertEqual(cm.exception.error_code, 1)
            handler.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.getvalue(), expected)
        patcher.stop()
