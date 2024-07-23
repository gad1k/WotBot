import sys
import pickle

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser
from config import Config
from exception import CredsException, InactiveChatException, InvalidTokenException, LoginException
from logger import CustomLogger


class WotBot:
    def __init__(self, config_path, log_path):
        self.config = Config(config_path)
        self.url = None
        self.username = None
        self.password = None
        self.token = None
        self.logger = CustomLogger(log_path)
        self.browser = Browser("Chrome", False)


    def config_props(self):
        self.logger.info("Config the bot properties")

        try:
            props = self.config.prepare_data()

            self.url = props["url"]
            self.username = props["username"]
            self.password = props["password"]
            self.token = props["token"]

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


    def stop_browser(self):
        if self.browser.engine is not None:
            self.logger.info("Stop the browser")
            self.browser.stop()


    def get_gift(self):
        self.logger.info("Open the required page")
        self.browser.engine.get(self.url)

        try:
            if not self.use_cookies():
                self.logger.info("Click on the login button")
                login = self.browser.engine.find_element(By.CSS_SELECTOR, "[data-cm-event='login']")
                login.click()

                self.logger.info("Waiting for a redirect")
                username = WebDriverWait(self.browser.engine, 30).until(ec.presence_of_element_located((By.ID, "id_login")))
                password = WebDriverWait(self.browser.engine, 30).until(ec.presence_of_element_located((By.ID, "id_password")))

                self.logger.info("Fill in the username and password")
                username.send_keys(self.username)
                password.send_keys(self.password)

                self.logger.info("Waiting for a login process")
                submit = self.browser.engine.find_element(By.CSS_SELECTOR, "button.button-airy")
                submit.click()

                self.check_login_status()
                self.save_cookies()

            self.logger.info("Try to get a gift")
            cur_item = self.browser.engine.find_element(By.CSS_SELECTOR, ".c_item.c_default")
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


    def check_gift_status(self):
        self.logger.info("Check the log for whether a gift has been received")

        if self.logger.check_logs():
            self.logger.warning("The gift has already been received")
            sys.exit()


    def check_login_status(self):
        try:
            login_status = WebDriverWait(self.browser.engine, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "p.js-form-errors-content")))
            if login_status is not None:
                raise LoginException()
        except TimeoutException:
            pass


    def use_cookies(self):
        self.logger.info("Try to upload and use the cookie file")
        try:
            for cookie in pickle.load(open(".cookies", "rb")):
                self.browser.engine.add_cookie(cookie)

            self.browser.engine.refresh()

            return True
        except FileNotFoundError:
            self.logger.warning("There is no cookie file")
            return False


    def save_cookies(self):
        self.logger.info("Save a cookie file")
        pickle.dump(self.browser.engine.get_cookies(), open(".cookies", "wb"))
