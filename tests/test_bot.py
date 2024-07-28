import os

from unittest import mock, TestCase
from selenium.webdriver import ChromeOptions

from modules.browser import Browser
from modules.config import Config
from modules.exception import CredsException, InactiveChatException, InvalidTokenException
from modules.logger import CustomLogger
from modules.bot import Bot


class TestBot(TestCase):
    def setUp(self):
        levels = ["info", "warning", "error"]

        self.mock_levels = {level: self.mock_log_level(CustomLogger, level) for level in levels}
        self.config_path = "dummy_config.json"
        self.log_path = "dummy_path.log"
        self.messages = [
            "Check the log for whether a gift has been received",
            "Config the bot properties",
            "Release resources",
            "Telegram bot is inactive",
            "Telegram token is incorrect",
            "The gift has already been received",
            "There is no such config file",
            "Username or password isn't set"
        ]

        self.bot = Bot(self.config_path, self.log_path)


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

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[0])
        mock_check_logs.assert_called_once()


    @mock.patch.object(CustomLogger, "check_logs")
    @mock.patch("sys.exit")
    def test_check_gift_status_positive(self, mock_exit, mock_check_logs):
        mock_check_logs.return_value = True

        self.bot.check_gift_status()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[0])
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, self.messages[5])
        mock_check_logs.assert_called_once()
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data", side_effect=CredsException)
    @mock.patch("sys.exit")
    def test_config_props_creds_exception(self, mock_exit, mock_prepare_data):
        self.bot.config_props()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[1])
        self.mock_levels["error"].assert_called_once_with(self.bot.logger, self.messages[7])
        mock_prepare_data.assert_called_once()
        mock_exit.assert_called_once()


    @mock.patch.object(Browser, "__init__")
    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InactiveChatException)
    def test_config_props_inactive_chat_exception(self, mock_add_telegram_handler, mock_prepare_data, mock_browser):
        mock_browser.return_value = None
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token",
            "headless": True
        }

        self.bot.config_props()

        self.assertEqual(self.mock_levels["info"].call_count, 2)
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, self.messages[3])
        mock_add_telegram_handler.assert_called_once_with("dummy_token")


    @mock.patch.object(Browser, "__init__")
    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler", side_effect=InvalidTokenException)
    def test_config_props_invalid_token_exception(self, mock_add_telegram_handler, mock_prepare_data, mock_browser):
        mock_browser.return_value = None
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token",
            "headless": True
        }

        self.bot.config_props()

        self.assertEqual(self.mock_levels["info"].call_count, 2)
        self.mock_levels["warning"].assert_called_once_with(self.bot.logger, self.messages[4])
        mock_add_telegram_handler.assert_called_once_with("dummy_token")


    @mock.patch("sys.exit")
    def test_config_props_file_not_found_exception(self, mock_exit):
        self.bot.config_props()

        self.assertRaises(FileNotFoundError, self.bot.config.prepare_data)
        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[1])
        self.mock_levels["error"].assert_called_once_with(self.bot.logger, self.messages[6])
        mock_exit.assert_called_once()


    @mock.patch.object(Config, "prepare_data")
    @mock.patch.object(CustomLogger, "add_telegram_handler")
    def test_config_props_with_th(self, mock_add_telegram_handler, mock_prepare_data):
        mock_prepare_data.return_value = {
            "driver": "Chrome",
            "url": "dummy_url",
            "username": "dummy_username",
            "password": "dummy_password",
            "token": "dummy_token",
            "headless": True
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
        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[1])
        mock_prepare_data.assert_called_once()


    @mock.patch("selenium.webdriver.Chrome")
    def test_release_resources(self, MockWebDriver):
        self.bot.browser = MockWebDriver

        self.bot.release_resources()

        self.mock_levels["info"].assert_called_once_with(self.bot.logger, self.messages[2])


    def test_set_options_headless_false(self):
        options = self.bot.set_options(False, ChromeOptions())

        self.assertEqual(options.arguments[0], "--window-size=1280,900")
        self.assertEqual(options.arguments[1], "--disable-gpu")
        self.assertEqual(options.arguments[2], "--log-level=3")
        self.assertEqual(options.arguments[3], "--ignore-certificate-errors")


    def test_set_options_headless_true(self):
        options = self.bot.set_options(True, ChromeOptions())

        self.assertEqual(options.arguments[0], "--headless")
        self.assertEqual(options.arguments[1], "--window-size=1280,900")
        self.assertEqual(options.arguments[2], "--disable-gpu")
        self.assertEqual(options.arguments[3], "--log-level=3")
        self.assertEqual(options.arguments[4], "--ignore-certificate-errors")
