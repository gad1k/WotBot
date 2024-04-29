import sys
import pickle

from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeService, ChromeOptions, EdgeService, EdgeOptions, FirefoxService, FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import Config
from exception import CredsException, InactiveChatException, InvalidTokenException, LoginException
from logger import CustomLogger


class WotBot:
    def __init__(self, path):
        self.config = Config(path)
        self.url = None
        self.username = None
        self.password = None
        self.token = None
        self.logger = CustomLogger()
        self.driver = None
        self.browser = None


    def config_props(self):
        self.logger.info("Config the bot properties")

        try:
            props = self.config.prepare_data()

            self.url = props["url"]
            self.username = props["username"]
            self.password = props["password"]
            self.token = props["token"]
            self.driver = props["driver"]

            if self.token:
                self.logger.info("Add telegram notification functionality")
                self.logger.add_telegram_handler(self.token)
        except CredsException:
            self.logger.error("Username or password isn't set")
            sys.exit()
        except InactiveChatException:
            self.logger.warning("Telegram bot is inactive")
        except InvalidTokenException:
            self.logger.warning("Telegram token is incorrect")
        except FileNotFoundError:
            self.logger.error("There is no such config file")
            sys.exit()


    def start_browser(self, headless: bool = True):
        self.logger.info("Start a browser")

        if self.driver == "Chrome":
            service = ChromeService(ChromeDriverManager().install())
            options = self.set_options(headless, ChromeOptions())

            self.browser = webdriver.Chrome(service=service, options=options)
        elif self.driver == "Edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            options = self.set_options(headless, EdgeOptions())

            self.browser = webdriver.Edge(service=service, options=options)
        else:
            service = FirefoxService(GeckoDriverManager().install())
            options = self.set_options(headless, FirefoxOptions())

            self.browser = webdriver.Firefox(service=service, options=options)


    def set_options(self, headless, options):
        if headless:
            options.add_argument("--headless")

        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")

        return options


    def stop_browser(self):
        if self.browser is not None:
            self.logger.info("Stop the browser")
            self.browser.quit()


    def get_gift(self):
        self.logger.info("Open the required page")
        self.browser.get(self.url)

        try:
            if not self.use_cookies():
                self.logger.info("Click on the login button")
                login = self.browser.find_element(By.CSS_SELECTOR, "[data-cm-event='login']")
                login.click()

                self.logger.info("Waiting for a redirect")
                username = WebDriverWait(self.browser, 30).until(ec.presence_of_element_located((By.ID, "id_login")))
                password = WebDriverWait(self.browser, 30).until(ec.presence_of_element_located((By.ID, "id_password")))

                self.logger.info("Fill in the username and password")
                username.send_keys(self.username)
                password.send_keys(self.password)

                self.logger.info("Waiting for a login process")
                submit = self.browser.find_element(By.CSS_SELECTOR, "button.button-airy")
                submit.click()

                self.check_login_status()
                self.save_cookies()

            self.logger.info("Try to get a gift")
            cur_item = self.browser.find_element(By.CSS_SELECTOR, ".c_item.c_default")
            cur_item.click()

            gift_desc = f"Your gift for today: {cur_item.text}"
            self.logger.info(gift_desc.replace("\n", " "))
        except LoginException:
            self.logger.error("The login process failed")
            self.stop_browser()
            sys.exit()
        except NoSuchElementException:
            self.logger.warning("The gift has already been received")
            self.stop_browser()
            sys.exit()


    def check_logs(self):
        self.logger.info("Check the log for whether a gift has been received")

        cur_date = datetime.today().strftime("%Y-%m-%d")
        with open("wot_bot.log") as file:
            logs = [line.strip() for line in file]

        for log in reversed(logs):
            items = log.split(" ", 3)
            if items[0] != cur_date:
                break
            if items[2] == "[INFO]":
                self.logger.warning("The gift has already been received")
                sys.exit()


    def check_login_status(self):
        try:
            login_status = WebDriverWait(self.browser, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "p.js-form-errors-content")))
            if login_status is not None:
                raise LoginException()
        except TimeoutException:
            pass


    def use_cookies(self):
        self.logger.info("Try to upload and use the cookie file")
        try:
            for cookie in pickle.load(open(".cookies", "rb")):
                self.browser.add_cookie(cookie)

            self.browser.refresh()

            return True
        except FileNotFoundError:
            self.logger.warning("There is no cookie file")
            return False


    def save_cookies(self):
        self.logger.info("Save a cookie file")
        pickle.dump(self.browser.get_cookies(), open(".cookies", "wb"))
