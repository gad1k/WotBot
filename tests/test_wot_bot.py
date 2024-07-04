import os

from unittest import mock, TestCase

from config import Config
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


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler")
    def test_config_props_with_th(self, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token"
        }

        self.bot.config_props()

        self.assertEqual(self.bot.url, "dummy_url")
        self.assertEqual(self.bot.username, "dummy_username")
        self.assertEqual(self.bot.password, "dummy_password")
        self.assertEqual(self.bot.token, "dummy_token")
        self.assertEqual(self.bot.driver, "Chrome")
        mock_prepare_data.assert_called_once()
        mock_add_telegram_handler.assert_called_once_with("dummy_token")


    @mock.patch.object(Config, "prepare_data")
    def test_config_props_without_th(self, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": ""
        }

        self.bot.config_props()

        self.assertEqual(self.bot.url, "dummy_url")
        self.assertEqual(self.bot.username, "dummy_username")
        self.assertEqual(self.bot.password, "dummy_password")
        self.assertEqual(self.bot.token, "")
        self.assertEqual(self.bot.driver, "Chrome")
        mock_prepare_data.assert_called_once()
