from unittest import mock, TestCase

from config import Config
from exception import CredsException


class TestConfig(TestCase):
    def test_check_data(self):
        data = {
            "username": "",
            "password": "dummy_password"
        }

        config = Config("dummy_path.json")

        with mock.patch.object(config, "data", data):
            self.assertRaises(CredsException, config.check_data)


    @mock.patch("builtins.open")
    @mock.patch("json.load")
    def test_prepare_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = {
            "username": "dummy_username",
            "password": "dummy_password"
        }

        config = Config("dummy_path.json")
        data = config.prepare_data()

        self.assertEqual(data["username"], "dummy_username")
        self.assertEqual(data["password"], "dummy_password")
        mock_open.assert_called_once_with("dummy_path.json")


    @mock.patch("builtins.open")
    @mock.patch("json.load")
    def test_upload_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = {
            "username": "dummy_username",
            "password": "dummy_password"
        }

        config = Config("dummy_path.json")
        config.upload_data()

        self.assertEqual(config.data["username"], "dummy_username")
        self.assertEqual(config.data["password"], "dummy_password")
        mock_open.assert_called_once_with("dummy_path.json")
        mock_json_load.assert_called_once()
