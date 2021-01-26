from click.testing import CliRunner

from evalai.add_token import set_token

from evalai.utils.config import LEN_OF_TOKEN
from evalai.utils.common import generate_random_string


class TestSetToken:
    def test_set_token(self):
        expected = "Success: Authentication token is successfully set."
        runner = CliRunner()
        result = runner.invoke(
            set_token, [generate_random_string(LEN_OF_TOKEN)])
        response = result.output.rstrip()
        assert response == expected
