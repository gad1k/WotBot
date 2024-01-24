import logging


class CustomFilter(logging.Filter):
    def filter(self, record):
        return record.module == "wot_bot"
