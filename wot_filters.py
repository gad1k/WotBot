import logging


class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.module == "wot_bot"


class FileFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().startswith("Your gift for today")
