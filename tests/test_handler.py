from unittest import mock, TestCase
import logging
from exporter import TelegramExporter
from handler import TelegramHandler


class TestExporter(TestCase):
    @mock.patch.object(TelegramExporter, "try_upload_cached_chat_id")
    @mock.patch.object(TelegramExporter, "try_retrieve_chat_id_remotely")
    @mock.patch.object(TelegramExporter, "send_message")
    def test_emit(self, mock_send_message, mock_try_retrieve_chat_id_remotely, mock_try_upload_cached_chat_id):
        handler = TelegramHandler("dummy_token")

        attrs = {
            "name": "dummy_name",
            "level": 2,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        handler.emit(logging.LogRecord(**attrs))

        mock_try_upload_cached_chat_id.assert_called_once()
        mock_try_retrieve_chat_id_remotely.assert_called_once()
        mock_send_message.assert_called_once()


    @mock.patch.object(TelegramExporter, "try_upload_cached_chat_id")
    @mock.patch.object(TelegramExporter, "try_retrieve_chat_id_remotely")
    def test_init_handler(self, try_retrieve_chat_id_remotely, mock_try_upload_cached_chat_id):
        handler = TelegramHandler("dummy_token")

        self.assertIsInstance(handler.telegram_exporter, TelegramExporter)
        mock_try_upload_cached_chat_id.assert_called_once()
        try_retrieve_chat_id_remotely.assert_called_once()
