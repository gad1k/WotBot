import logging


class CommonFilter(logging.Filter):
    def filter(self, record):
        return (record.getMessage().startswith("Your gift for today") or   # noqa
                record.levelname == "ERROR")


class StreamFilter(logging.Filter):
    def filter(self, record):
        return record.module == "bot"
