from unittest import mock, TestCase
from requests.models import Response

from exporter import TelegramExporter


class TestExporter(TestCase):
    def test_file_not_found(self):
        exporter = TelegramExporter("dummy_token")
        exporter.try_upload_cached_chat_id()


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save_settings(self, mock_open):
        exporter = TelegramExporter("dummy_token")

        with mock.patch.object(exporter, "chat_id", "dummy_chat_id"):
            exporter.save_settings()

        mock_open.assert_called_once_with(".settings", "w", encoding="utf-8")
        mock_open().write.assert_called_once_with("dummy_chat_id")


    @mock.patch("requests.get")
    def test_send_message(self, mock_get):
        exporter = TelegramExporter("dummy_token")

        mock_get.return_value = "dummy_response"
        with mock.patch.object(exporter, "chat_id", "dummy_chat_id"):
            exporter.send_message("dummy_text")

        expected_result = "https://api.telegram.org/botdummy_token/sendMessage?chat_id=dummy_chat_id&text=dummy_text"
        mock_get.assert_called_once_with(expected_result)


    @mock.patch.object(TelegramExporter, "save_settings")
    @mock.patch("requests.get")
    def test_try_retrieve_chat_id_remotely(self, mock_get, mock_save_settings):
        exporter = TelegramExporter("dummy_token")

        response = mock.MagicMock(spec=Response)
        response.json.return_value = {"result": [{"message": {"chat": {"id": "dummy_chat_id"}}}]}
        mock_get.return_value = response

        exporter.try_retrieve_chat_id_remotely()

        self.assertEqual(exporter.chat_id, "dummy_chat_id")
        mock_get.assert_called_once_with("https://api.telegram.org/botdummy_token/getUpdates")
        mock_save_settings.assert_called_once()


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_try_upload_cached_chat_id(self, mock_open):
        exporter = TelegramExporter("dummy_token")

        mock_open.return_value.readline.return_value = "dummy_token"

        exporter.try_upload_cached_chat_id()

        self.assertEqual(exporter.chat_id, "dummy_token")
        mock_open.assert_called_once_with(".settings")
