import os

from unittest import mock, TestCase

from config import Config
from exception import CredsException, InactiveChatException, InvalidTokenException
from logger import CustomLogger
from wot_bot import WotBot


class TestWotBot(TestCase):
    def setUp(self):
        self.config_path = "dummy_config.json"
        self.log_path = "dummy_path.log"

        info_patcher = mock.patch.object(CustomLogger, "info", autospec=True)
        self.mock_log_info = info_patcher.start()
        self.addCleanup(info_patcher.stop)

        warning_patcher = mock.patch.object(CustomLogger, "warning", autospec=True)
        self.mock_log_warning = warning_patcher.start()
        self.addCleanup(warning_patcher.stop)

        self.bot = WotBot(self.config_path, self.log_path)


    def tearDown(self):
        self.bot.logger.handlers[1].close()

        if os.path.exists(self.log_path):
            os.remove(self.log_path)


    @mock.patch.object(CustomLogger, "check_logs")
    def test_check_gift_status_negative(self, mock_check_logs):
        mock_check_logs.return_value = False

        self.bot.check_gift_status()

        self.mock_log_info.assert_called_once_with(self.bot.logger, "Check the log for whether a gift has been received")
        mock_check_logs.assert_called_once()


    @mock.patch.object(CustomLogger, "check_logs")
    @mock.patch("sys.exit")
    def test_check_gift_status_positive(self, mock_exit, mock_check_logs):
        mock_check_logs.return_value = True

        self.bot.check_gift_status()

        self.mock_log_info.assert_called_once_with(self.bot.logger, "Check the log for whether a gift has been received")
        mock_check_logs.assert_called_once()
        self.mock_log_warning.assert_called_once_with(self.bot.logger, "The gift has already been received")
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data", side_effect=CredsException)
    @mock.patch.object(CustomLogger, "error")
    @mock.patch.object(CustomLogger, "info")
    @mock.patch("sys.exit")
    def test_config_props_creds_exception(self, mock_exit, mock_log_info, mock_log_error, mock_prepare_data):
        self.bot.config_props()

        mock_log_info.assert_called_once_with("Config the bot properties")
        mock_prepare_data.assert_called_once()
        mock_log_error.assert_called_once_with("Username or password isn't set")
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InactiveChatException)
    @mock.patch.object(CustomLogger, "warning")
    @mock.patch.object(CustomLogger, "info")
    def test_config_props_inactive_chat_exception(self, mock_log_info, mock_log_warning, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token"
        }

        self.bot.config_props()

        self.assertEqual(mock_log_info.call_count, 2)
        mock_add_telegram_handler.assert_called_once_with("dummy_token")
        mock_log_warning.assert_called_once_with("Telegram bot is inactive")


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InvalidTokenException)
    @mock.patch.object(CustomLogger, "warning")
    @mock.patch.object(CustomLogger, "info")
    def test_config_props_invalid_token_exception(self, mock_log_info, mock_log_warning, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token"
        }

        self.bot.config_props()

        self.assertEqual(mock_log_info.call_count, 2)
        mock_add_telegram_handler.assert_called_once_with("dummy_token")
        mock_log_warning.assert_called_once_with("Telegram token is incorrect")


    @mock.patch.object(CustomLogger, "error")
    @mock.patch.object(CustomLogger, "info")
    @mock.patch("sys.exit")
    def test_config_props_file_not_found_exception(self, mock_exit, mock_log_info, mock_log_error):
        self.bot.config_props()

        self.assertRaises(FileNotFoundError, self.bot.config.prepare_data)
        mock_log_info.assert_called_once_with("Config the bot properties")
        mock_log_error.assert_called_once_with("There is no such config file")
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
