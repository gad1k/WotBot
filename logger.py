import sys
import logging

from filter import CommonFilter, StreamFilter
from formatter import FileFormatter, StreamFormatter
from handler import TelegramHandler


class CustomLogger(logging.Logger):
    def __init__(self):
        super().__init__(name=__name__, level=logging.INFO)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.addFilter(StreamFilter())
        stream_handler.setFormatter(StreamFormatter())

        file_handler = logging.FileHandler("wot_bot.log")
        file_handler.addFilter(CommonFilter())
        file_handler.setFormatter(FileFormatter())

        self.addHandler(stream_handler)
        self.addHandler(file_handler)
        self.setLevel(logging.INFO)


    def add_telegram_handler(self, token):
        telegram_handler = TelegramHandler(token)
        telegram_handler.addFilter(CommonFilter())

        self.addHandler(telegram_handler)
