import mock

from io import StringIO
from unittest import TestCase

from evalai.utils.config import HOST_URL_FILE_PATH


class TestWriteHostUrlToFile(TestCase):
    def setUp(self):
        self.new_host = "http://testserver.abc"

    @mock.patch("evalai.utils.auth.open", new=mock.mock_open())
    def test_write_host_url_to_file_success(self, mock_open):
        expected = "{} is set as the host url.\n".format(self.new_host)
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            write_host_url_to_file(self.new_host)
            mock_open.assert_called_with(HOST_URL_FILE_PATH, "w")
            mock_open.write.assert_called_with(self.new_host)
            self.assertEqual(fake_out.get_value(), expected)

    @mock.patch("evalai.utils.auth.open", new=mock.mock_open())
    def test_write_host_url_to_file_fail(self, mock_open):
        mock_open.write.side_effect = OSError("Permission denied.")
        expected = "Permission denied.\nNone\n"
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                write_host_url_to_file(self.new_host)
                self.assertEqual(cm.exception.error_code, 1)
            self.assertEqual(fake_out.get_value(), expected)
