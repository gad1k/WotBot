from unittest import mock, TestCase

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriverChrome
from selenium.webdriver.edge.webdriver import WebDriver as WebDriverEdge
from selenium.webdriver.firefox.webdriver import WebDriver as WebDriverFirefox

from modules.browser import Browser
from modules.cookie import Cookie


class TestBrowser(TestCase):
    @mock.patch.object(Browser, "init_engine")
    def setUp(self, mock_init_engine):
        self.browser = Browser("Chrome", True)


    def tearDown(self):
        if self.browser.engine is not None:
            self.browser.engine.quit()


    @mock.patch("selenium.webdriver.Chrome")
    def test_check_engine_initialized(self, mock_web_driver):
        self.browser.engine = mock_web_driver

        self.assertTrue(self.browser.headless)
        self.assertTrue(self.browser.check_engine_initialized())


    @mock.patch("selenium.webdriver.Chrome")
    def test_get_engine(self, mock_web_driver):
        self.browser.engine = mock_web_driver

        self.assertTrue(self.browser.headless)
        self.assertEqual(self.browser.get_engine(), mock_web_driver)


    def test_init_engine_chrome(self):
        browser = Browser("Chrome", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverChrome)

        if browser.engine is not None:
            browser.engine.quit()


    def test_init_engine_edge(self):
        browser = Browser("Edge", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverEdge)

        if browser.engine is not None:
            browser.engine.quit()


    def test_init_engine_firefox(self):
        browser = Browser("Firefox", True)

        self.assertTrue(browser.headless)
        self.assertIsInstance(browser.engine, WebDriverFirefox)

        if browser.engine is not None:
            browser.engine.quit()


    @mock.patch.object(Cookie, "save")
    def test_save_cookies(self, mock_save):
        self.browser.save_cookies()

        self.assertTrue(self.browser.headless)
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

        if browser.engine is not None:
            browser.engine.quit()


    def test_set_options_headless_true(self):
        options = self.browser.set_options(ChromeOptions(), self.browser.headless)

        self.assertTrue(self.browser.headless)
        self.assertEqual(options.arguments[0], "--headless")
        self.assertEqual(options.arguments[1], "--window-size=1280,900")
        self.assertEqual(options.arguments[2], "--disable-gpu")
        self.assertEqual(options.arguments[3], "--log-level=3")
        self.assertEqual(options.arguments[4], "--ignore-certificate-errors")


    def test_stop_engine(self):
        self.browser.stop_engine()

        self.assertTrue(self.browser.headless)


    @mock.patch.object(Cookie, "use")
    def test_use_cookies(self, mock_use):
        self.assertTrue(self.browser.headless)
        self.assertTrue(self.browser.use_cookies())
        mock_use.assert_called_once()


    @mock.patch.object(Cookie, "use", side_effect=FileNotFoundError)
    def test_use_cookies_catch_file_not_found_error(self, mock_use):
        self.assertTrue(self.browser.headless)
        self.assertFalse(self.browser.use_cookies())
        mock_use.assert_called_once()
