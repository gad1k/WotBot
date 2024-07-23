from selenium import webdriver
from selenium.webdriver import ChromeService, ChromeOptions, EdgeService, EdgeOptions, FirefoxService, FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class Browser:
    def __init__(self, driver, headless=True):
        self.engine = self.init_engine(driver, headless)
        self.cookie = None


    def init_engine(self, driver, headless):
        if driver == "Chrome":
            service = ChromeService(ChromeDriverManager().install())
            options = self.set_options(headless, ChromeOptions())

            engine = webdriver.Chrome(service=service, options=options)
        elif driver == "Edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            options = self.set_options(headless, EdgeOptions())

            engine = webdriver.Edge(service=service, options=options)
        else:
            service = FirefoxService(GeckoDriverManager().install())
            options = self.set_options(headless, FirefoxOptions())

            engine = webdriver.Firefox(service=service, options=options)

        return engine


    def set_options(self, headless, options):
        if headless:
            options.add_argument("--headless")

        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")

        return options


    def stop(self):
        if self.engine is not None:
            self.engine.quit()
