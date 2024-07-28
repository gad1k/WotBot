from unittest import mock, TestCase

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriverChrome
from selenium.webdriver.edge.webdriver import WebDriver as WebDriverEdge
from selenium.webdriver.firefox.webdriver import WebDriver as WebDriverFirefox

from modules.browser import Browser
from modules.cookie import Cookie


class TestBrowser(TestCase):
    @mock.patch.object(Browser, "init_engine")
    @mock.patch("selenium.webdriver.Chrome")
    def test_check_engine_initialized(self, mock_web_driver, mock_init_engine):
        browser = Browser("Chrome", True)
        browser.engine = mock_web_driver

        self.assertTrue(browser.headless)
        self.assertTrue(browser.check_engine_initialized())
        mock_init_engine.assert_called_once_with("Chrome")


    @mock.patch.object(Browser, "init_engine")
    @mock.patch("selenium.webdriver.Chrome")
    def test_get_engine(self, mock_web_driver, mock_init_engine):
        browser = Browser("Chrome", True)
        browser.engine = mock_web_driver

        self.assertTrue(browser.headless)
        self.assertEqual(browser.get_engine(), mock_web_driver)
        mock_init_engine.assert_called_once_with("Chrome")


    def test_init_engine_chrome(self):
        browser = Browser("Chrome", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverChrome)


    def test_init_engine_edge(self):
        browser = Browser("Edge", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverEdge)


    def test_init_engine_firefox(self):
        browser = Browser("Firefox", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverFirefox)


    @mock.patch.object(Browser, "init_engine")
    @mock.patch.object(Cookie, "save")
    def test_save_cookies(self, mock_save, mock_init_engine):
        browser = Browser("Chrome", True)
        browser.save_cookies()

        self.assertTrue(browser.headless)
        mock_init_engine.assert_called_once_with("Chrome")
        mock_save.assert_called_once()


    @mock.patch.object(Browser, "init_engine")
    def test_set_options_headless_false(self, mock_init_engine):
        browser = Browser("Chrome", False)
        options = browser.set_options(ChromeOptions(), browser.headless)

        self.assertFalse(browser.headless)
        self.assertEqual(options.arguments[0], "--window-size=1280,900")
        self.assertEqual(options.arguments[1], "--disable-gpu")
        self.assertEqual(options.arguments[2], "--log-level=3")
        self.assertEqual(options.arguments[3], "--ignore-certificate-errors")
        mock_init_engine.assert_called_once_with("Chrome")


    @mock.patch.object(Browser, "init_engine")
    def test_set_options_headless_true(self, mock_init_engine):
        browser = Browser("Chrome", True)
        options = browser.set_options(ChromeOptions(), browser.headless)

        self.assertTrue(browser.headless)
        self.assertEqual(options.arguments[0], "--headless")
        self.assertEqual(options.arguments[1], "--window-size=1280,900")
        self.assertEqual(options.arguments[2], "--disable-gpu")
        self.assertEqual(options.arguments[3], "--log-level=3")
        self.assertEqual(options.arguments[4], "--ignore-certificate-errors")
        mock_init_engine.assert_called_once_with("Chrome")


    @mock.patch.object(Browser, "init_engine")
    def test_stop_engine(self, mock_init_engine):
        browser = Browser("Chrome", True)
        browser.stop_engine()

        self.assertTrue(browser.headless)
        mock_init_engine.assert_called_once_with("Chrome")


    @mock.patch.object(Browser, "init_engine")
    @mock.patch.object(Cookie, "use")
    def test_use_cookies(self, mock_use, mock_init_engine):
        browser = Browser("Chrome", True)

        self.assertTrue(browser.headless)
        self.assertTrue(browser.use_cookies())
        mock_init_engine.assert_called_once_with("Chrome")
        mock_use.assert_called_once()


    @mock.patch.object(Browser, "init_engine")
    @mock.patch.object(Cookie, "use", side_effect=FileNotFoundError)
    def test_use_cookies_catch_file_not_found_error(self, mock_use, mock_init_engine):
        browser = Browser("Chrome", True)

        self.assertTrue(browser.headless)
        self.assertFalse(browser.use_cookies())
        mock_init_engine.assert_called_once_with("Chrome")
        mock_use.assert_called_once()
