from selenium import webdriver
from selenium.webdriver import ChromeService, ChromeOptions, EdgeService, EdgeOptions, FirefoxService, FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from cookie import Cookie


class Browser:
    def __init__(self, driver, headless):
        self.engine = self.init_engine(driver, headless)
        self.cookie = Cookie(self.engine)


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


    def check_engine_initialized(self):
        return self.engine is not None


    def stop_engine(self):
        self.engine.quit()


    def get_engine(self):
        return self.engine


    def use_cookies(self):
        try:
            self.cookie.use()
            self.engine.refresh()
            return True
        except FileNotFoundError:
            return False


    def save_cookies(self):
        self.cookie.save()
