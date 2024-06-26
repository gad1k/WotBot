import sys
import logging

from datetime import datetime, timedelta
from filter import CommonFilter, StreamFilter
from formatter import FileFormatter, StreamFormatter
from handler import TelegramHandler


class CustomLogger(logging.Logger):
    def __init__(self, path):
        super().__init__(name=__name__, level=logging.INFO)
        self.log_path = path
        self.fmt_dt = "%Y-%m-%d"

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


    def check_logs(self):
        cur_date = datetime.today().strftime(self.fmt_dt)

        for log in self.read_logs():
            items = log.split(" ", 3)
            log_date = self.convert_to_utc(" ".join(items[:2]))

            if log_date == cur_date and items[2] == "[INFO]":
                return True

        return False


    def read_logs(self):
        with open(self.log_path) as file:
            for line in file:
                yield line.strip()


    def convert_to_utc(self, log_ts):
        fmt_ts = "%Y-%m-%d %H:%M:%S,%f"
        utc_log_ts = datetime.strptime(log_ts, fmt_ts) - timedelta(hours=3)

        return utc_log_ts.strftime(self.fmt_dt)
