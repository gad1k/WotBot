import sys
import logging

from filter import CommonFilter, ConsoleFilter
from formatter import CommonFormatter
from handler import TelegramHandler


class CustomLogger(logging.Logger):
    def __init__(self):
        super().__init__(name=__name__, level=logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.addFilter(ConsoleFilter())
        console_handler.setFormatter(CommonFormatter())

        file_handler = logging.FileHandler("wot_bot.log")
        file_handler.addFilter(CommonFilter())
        file_handler.setFormatter(CommonFormatter())

        self.addHandler(console_handler)
        self.addHandler(file_handler)
        self.setLevel(logging.INFO)


    def add_telegram_handler(self, token):
        telegram_handler = TelegramHandler(token)
        telegram_handler.addFilter(CommonFilter())

        self.addHandler(telegram_handler)
