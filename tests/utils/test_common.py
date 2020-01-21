from unittest.mock import patch, mock_open
from evalai.utils.common import store_data_to_json

from ..base import BaseTestClass


@patch("evalai.utils.common.json.dump")
@patch("evalai.utils.common.click.echo")
class TestStoreDataToJson(BaseTestClass):
    def setup(self):
        self.path = "test_path"
        self.content = "test content"
        self.message = "test message"

    def test_store_data_to_json(self, mock_echo, mock_dump):
        mock_file = mock_open()
        with patch("evalai.utils.common.open", mock_file):
            store_data_to_json(self.path, self.content, self.message)
            mock_dump.assert_called()
            mock_echo.assert_not_called()

    def test_store_data_to_json_when_error_is_raised(self, mock_dump, mock_echo):
        mock_dump.side_effect = OSError("Exception")
        mock_file = mock_open()
        with patch("evalai.utils.common.open", mock_file):
            store_data_to_json(self.path, self.content, self.message)
            mock_echo.assert_called()
