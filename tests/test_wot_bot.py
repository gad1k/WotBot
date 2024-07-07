import os

from unittest import mock, TestCase

from config import Config
from exception import CredsException, InactiveChatException, InvalidTokenException
from logger import CustomLogger
from wot_bot import WotBot


class TestWotBot(TestCase):
    def setUp(self):
        levels = ["info", "warning", "error"]

        self.mock_levels = {level: self.mock_log_level(CustomLogger, level) for level in levels}
        self.config_path = "dummy_config.json"
        self.log_path = "dummy_path.log"
        self.messages = [

        ]

        self.bot = WotBot(self.config_path, self.log_path)


    def tearDown(self):
        self.bot.logger.handlers[1].close()

        if os.path.exists(self.log_path):
            os.remove(self.log_path)


    def mock_log_level(self, logger, level):
        patcher = mock.patch.object(logger, level, autospec=True)
        mock_level = patcher.start()
        self.addCleanup(patcher.stop)

        return mock_level


    @mock.patch.object(CustomLogger, "check_logs")
    def test_check_gift_status_negative(self, mock_check_logs):
        mock_check_logs.return_value = False

        self.bot.check_gift_status()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, "Check the log for whether a gift has been received")
        mock_check_logs.assert_called_once()


    @mock.patch.object(CustomLogger, "check_logs")
    @mock.patch("sys.exit")
    def test_check_gift_status_positive(self, mock_exit, mock_check_logs):
        mock_check_logs.return_value = True

        self.bot.check_gift_status()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, "Check the log for whether a gift has been received")
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, "The gift has already been received")
        mock_check_logs.assert_called_once()
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data", side_effect=CredsException)
    @mock.patch("sys.exit")
    def test_config_props_creds_exception(self, mock_exit, mock_prepare_data):
        self.bot.config_props()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, "Config the bot properties")
        self.mock_levels["error"].assert_called_once_with(self.bot.logger, "Username or password isn't set")
        mock_prepare_data.assert_called_once()
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InactiveChatException)
    def test_config_props_inactive_chat_exception(self, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token"
        }

        self.bot.config_props()

        self.assertEqual(self.mock_levels["info"].call_count, 2)
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, "Telegram bot is inactive")
        mock_add_telegram_handler.assert_called_once_with("dummy_token")


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InvalidTokenException)
    def test_config_props_invalid_token_exception(self, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token"
        }

        self.bot.config_props()

        self.assertEqual(self.mock_levels["info"].call_count, 2)
        mock_add_telegram_handler.assert_called_once_with("dummy_token")
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, "Telegram token is incorrect")


    @mock.patch("sys.exit")
    def test_config_props_file_not_found_exception(self, mock_exit):
        self.bot.config_props()

        self.assertRaises(FileNotFoundError, self.bot.config.prepare_data)
        self.mock_levels["info"].assert_called_once_with(self.bot.logger, "Config the bot properties")
        self.mock_levels["error"].assert_called_once_with(self.bot.logger, "There is no such config file")
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
        self.assertEqual(self.mock_levels["info"].call_count, 2)
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
        self.mock_levels["info"].assert_called_once_with(self.bot.logger, "Config the bot properties")
        mock_prepare_data.assert_called_once()
