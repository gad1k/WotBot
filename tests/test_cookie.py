import pickle

from unittest import mock, TestCase

from modules.cookie import Cookie


class TestCookie(TestCase):
    @mock.patch("selenium.webdriver.Chrome")
    def setUp(self, mock_web_driver):
        self.cookie = Cookie(mock_web_driver)


    @mock.patch.object(pickle, "dump")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save(self, mock_open, mock_dump):
        self.cookie.save()

        mock_open.assert_called_once_with("../settings/cookies", "wb")
        mock_dump.assert_called_once()


    @mock.patch.object(pickle, "load")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_use(self, mock_open, mock_load):
        mock_load.return_value = {
            "dummy_key": "dummy_value"
        }

        self.cookie.use()

        mock_open.assert_called_once_with("../settings/cookies", "rb")
        mock_load.assert_called_once()
