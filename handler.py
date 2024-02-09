import sys
import logging

from exporter import TelegramExporter


class TelegramHandler(logging.FileHandler):
    def __init__(self, token):
        logging.Handler.__init__(self)
        self.stream = sys.stdout

        self.telegram_exporter = TelegramExporter(token)
        self.telegram_exporter.retrieve_chat_id()


    def emit(self, record):
        self.telegram_exporter.send_message(self.format(record))
