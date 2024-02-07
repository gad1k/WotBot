import logging


class CommonFilter(logging.Filter):
    def filter(self, record):
        return (record.getMessage().startswith("Your gift for today") or
                record.levelname == "ERROR")


class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.module == "wot_bot"
