import sys
import logging

from datetime import datetime
from filter import CommonFilter, StreamFilter
from formatter import FileFormatter, StreamFormatter
from handler import TelegramHandler


class CustomLogger(logging.Logger):
    def __init__(self):
        super().__init__(name=__name__, level=logging.INFO)
        self.log_path = "wot_bot.log"

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.addFilter(StreamFilter())
        stream_handler.setFormatter(StreamFormatter())

        file_handler = logging.FileHandler(self.log_path)
        file_handler.addFilter(CommonFilter())
        file_handler.setFormatter(FileFormatter())

        self.addHandler(stream_handler)
        self.addHandler(file_handler)
        self.setLevel(logging.INFO)


    def add_telegram_handler(self, token):
        telegram_handler = TelegramHandler(token)
        telegram_handler.addFilter(CommonFilter())

        self.addHandler(telegram_handler)


    def check_gift_received(self):
        cur_date = datetime.today().strftime("%Y-%m-%d")

        with open(self.log_path) as file:
            logs = [line.strip() for line in file]

        for log in reversed(logs):
            items = log.split(" ", 3)
            if items[0] != cur_date:
                break
            if items[2] == "[INFO]":
                return True

        return False
