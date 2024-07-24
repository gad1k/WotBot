from unittest import mock, TestCase
from requests.models import Response

from modules.exporter import TelegramExporter
from modules.exception import InactiveChatException, InvalidTokenException


class TestExporter(TestCase):
    def setUp(self):
        self.exporter = TelegramExporter("dummy_token")
        self.response = mock.MagicMock(spec=Response)


    @mock.patch("requests.get")
    def test_exception_inactive_chat(self, mock_get):
        self.response.json.return_value = {"result": []}
        mock_get.return_value = self.response

        self.assertRaises(InactiveChatException, self.exporter.try_retrieve_chat_id_remotely)
        mock_get.assert_called_once_with("https://api.telegram.org/botdummy_token/getUpdates")


    @mock.patch("requests.get")
    def test_exception_invalid_token(self, mock_get):
        self.response.json.return_value = {"error_code": 404}
        mock_get.return_value = self.response

        self.assertRaises(InvalidTokenException, self.exporter.try_retrieve_chat_id_remotely)
        mock_get.assert_called_once_with("https://api.telegram.org/botdummy_token/getUpdates")


    def test_exception_missing_cookie(self):
        self.exporter.try_upload_cached_chat_id()


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save_settings(self, mock_open):
        with mock.patch.object(self.exporter, "chat_id", "dummy_chat_id"):
            self.exporter.save_settings()

        mock_open.assert_called_once_with(".settings", "w", encoding="utf-8")
        mock_open().write.assert_called_once_with("dummy_chat_id")


    @mock.patch("requests.get")
    def test_send_message(self, mock_get):
        mock_get.return_value = "dummy_response"
        with mock.patch.object(self.exporter, "chat_id", "dummy_chat_id"):
            self.exporter.send_message("dummy_text")

        expected_result = "https://api.telegram.org/botdummy_token/sendMessage?chat_id=dummy_chat_id&text=dummy_text"
        mock_get.assert_called_once_with(expected_result)


    @mock.patch.object(TelegramExporter, "save_settings")
    @mock.patch("requests.get")
    def test_try_retrieve_chat_id_remotely(self, mock_get, mock_save_settings):
        self.response.json.return_value = {"result": [{"message": {"chat": {"id": "dummy_chat_id"}}}]}
        mock_get.return_value = self.response

        self.exporter.try_retrieve_chat_id_remotely()

        self.assertEqual(self.exporter.chat_id, "dummy_chat_id")
        mock_get.assert_called_once_with("https://api.telegram.org/botdummy_token/getUpdates")
        mock_save_settings.assert_called_once()


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_try_upload_cached_chat_id(self, mock_open):
        mock_open.return_value.readline.return_value = "dummy_token"

        self.exporter.try_upload_cached_chat_id()

        self.assertEqual(self.exporter.chat_id, "dummy_token")
        mock_open.assert_called_once_with(".settings")
