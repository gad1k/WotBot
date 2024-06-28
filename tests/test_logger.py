import handler
import logging
import os

from datetime import datetime
from unittest import mock, TestCase

from exporter import TelegramExporter
from logger import CustomLogger


class TestLogger(TestCase):
    @mock.patch.object(TelegramExporter, "try_upload_cached_chat_id")
    @mock.patch.object(TelegramExporter, "try_retrieve_chat_id_remotely")
    def test_add_telegram_handler(self, mock_try_retrieve_chat_id_remotely, mock_try_upload_cached_chat_id):
        path = "dummy_path.log"

        logger = CustomLogger(path)
        logger.add_telegram_handler("dummy_token")

        self.assertEqual(len(logger.handlers), 3)
        self.assertIsInstance(logger.handlers[2], handler.TelegramHandler)
        mock_try_upload_cached_chat_id.assert_called_once()
        mock_try_retrieve_chat_id_remotely.assert_called_once()

        logger.handlers[1].close()

        if os.path.exists(path):
            os.remove(path)


    @mock.patch.object(CustomLogger, "init_default_handlers")
    @mock.patch.object(CustomLogger, "read_logs")
    @mock.patch.object(CustomLogger, "convert_to_utc")
    @mock.patch("logger.datetime")
    def test_check_logs_false(self, mock_datetime, mock_convert_to_utc, mock_read_logs, mock_init_default_handlers):
        logger = CustomLogger("dummy_path.log")

        mock_datetime.today.return_value = datetime(2024, 6, 27)
        mock_read_logs.return_value = ["2024-06-27 14:12:40,451 [ERROR] Failure"]
        mock_convert_to_utc.return_value = "2024-06-27"

        self.assertEqual(logger.check_logs(), False)
        mock_init_default_handlers.assert_called_once()
        mock_read_logs.assert_called_once()
        mock_convert_to_utc.assert_called_once_with("2024-06-27 14:12:40,451")


    @mock.patch.object(CustomLogger, "init_default_handlers")
    @mock.patch.object(CustomLogger, "read_logs")
    @mock.patch.object(CustomLogger, "convert_to_utc")
    @mock.patch("logger.datetime")
    def test_check_logs_true(self, mock_datetime, mock_convert_to_utc, mock_read_logs, mock_init_default_handlers):
        logger = CustomLogger("dummy_path.log")

        mock_datetime.today.return_value = datetime(2024, 6, 27)
        mock_read_logs.return_value = ["2024-06-27 14:12:40,451 [INFO] Success"]
        mock_convert_to_utc.return_value = "2024-06-27"

        self.assertEqual(logger.check_logs(), True)
        mock_init_default_handlers.assert_called_once()
        mock_read_logs.assert_called_once()
        mock_convert_to_utc.assert_called_once_with("2024-06-27 14:12:40,451")


    @mock.patch.object(CustomLogger, "init_default_handlers")
    def test_convert_to_utc(self, mock_init_default_handlers):
        logger = CustomLogger("dummy_path.log")

        self.assertEqual(logger.convert_to_utc("2024-06-26 01:12:40,451"), "2024-06-25")
        mock_init_default_handlers.assert_called_once()


    def test_init_default_handlers(self):
        path = "dummy_path.log"

        logger = CustomLogger(path)

        self.assertEqual(len(logger.handlers), 2)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
        self.assertIsInstance(logger.handlers[1], logging.FileHandler)

        logger.handlers[1].close()

        if os.path.exists(path):
            os.remove(path)


    @mock.patch.object(CustomLogger, "init_default_handlers")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_read_logs(self, mock_open, mock_init_default_handlers):
        logger = CustomLogger("dummy_path.log")

        file_content = (
            "2024-06-26 01:12:40,451 [ERROR] The login process failed\n"
            "2024-06-26 13:12:30,492 [ERROR] The login process failed\n"
        )
        mock_open.return_value.__enter__.return_value = iter(file_content.splitlines(True))

        result = [
            "2024-06-26 01:12:40,451 [ERROR] The login process failed",
            "2024-06-26 13:12:30,492 [ERROR] The login process failed"
        ]
        self.assertEqual(list(logger.read_logs()), result)
        mock_init_default_handlers.assert_called_once()
