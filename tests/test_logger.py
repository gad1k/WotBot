from unittest import mock, TestCase

from datetime import datetime
from logger import CustomLogger


class TestLogger(TestCase):
    @mock.patch.object(CustomLogger, "init_default_handlers")
    @mock.patch.object(CustomLogger, "read_logs")
    @mock.patch.object(CustomLogger, "convert_to_utc")
    @mock.patch("logger.datetime")
    def test_check_logs_1(self, mock_datetime, mock_convert_to_utc, mock_read_logs, mock_init_default_handlers):
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
    def test_check_logs_2(self, mock_datetime, mock_convert_to_utc, mock_read_logs, mock_init_default_handlers):
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
