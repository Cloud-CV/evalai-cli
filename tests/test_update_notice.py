from unittest.mock import patch

from click.testing import CliRunner

from evalai.main import main


class TestUpdateNotice:
    def test_outdated_version_prints_update_notice_without_crash(self):
        runner = CliRunner()
        with patch('evalai.main.get_latest_version', return_value='9999.0.0'), \
            patch('evalai.main.__version__', '0.0.0'):
            result = runner.invoke(main, [])
        assert isinstance(result.exception, SystemExit)
        assert result.exit_code == 1
        assert 'Please install the latest version of EvalAI-CLI!' in result.output
        assert 'Use: pip install --upgrade evalai' in result.output
