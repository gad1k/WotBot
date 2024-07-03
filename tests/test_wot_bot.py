import os

from unittest import mock, TestCase

from logger import CustomLogger
from wot_bot import WotBot


class TestWotBot(TestCase):
    def setUp(self):
        self.config_path = "dummy_config.json"
        self.log_path = "dummy_path.log"

        self.bot = WotBot(self.config_path, self.log_path)


    def tearDown(self):
        self.bot.logger.handlers[1].close()

        if os.path.exists(self.log_path):
            os.remove(self.log_path)


    @mock.patch.object(CustomLogger, "check_logs")
    def test_check_gift_status_negative(self, mock_check_logs):
        mock_check_logs.return_value = False

        self.bot.check_gift_status()
        mock_check_logs.assert_called_once()


    @mock.patch.object(CustomLogger, "check_logs")
    @mock.patch("sys.exit")
    def test_check_gift_status_positive(self, mock_exit, mock_check_logs):
        mock_check_logs.return_value = True

        self.bot.check_gift_status()
        mock_check_logs.assert_called_once()
        mock_exit.assert_called_once()
