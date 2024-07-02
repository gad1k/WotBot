import logging

from unittest import mock, TestCase

from exporter import TelegramExporter
from handler import TelegramHandler


class TestExporter(TestCase):
    @mock.patch.object(TelegramExporter, "try_upload_cached_chat_id")
    @mock.patch.object(TelegramExporter, "try_retrieve_chat_id_remotely")
    def setUp(self, mock_try_retrieve_chat_id_remotely, mock_try_upload_cached_chat_id):
        self.handler = TelegramHandler("dummy_token")

        mock_try_upload_cached_chat_id.assert_called_once()
        mock_try_retrieve_chat_id_remotely.assert_called_once()


    @mock.patch.object(TelegramExporter, "send_message")
    def test_emit(self, mock_send_message):
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        self.handler.emit(logging.LogRecord(**attrs))
        mock_send_message.assert_called_once()


    def test_init_handler(self):
        self.assertIsInstance(self.handler.telegram_exporter, TelegramExporter)
