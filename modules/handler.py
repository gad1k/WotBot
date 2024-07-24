import sys
import logging

from modules.exporter import TelegramExporter


class TelegramHandler(logging.FileHandler):
    def __init__(self, token):
        logging.Handler.__init__(self)
        self.stream = sys.stdout

        self.telegram_exporter = TelegramExporter(token)
        self.telegram_exporter.try_upload_cached_chat_id()
        self.telegram_exporter.try_retrieve_chat_id_remotely()


    def emit(self, record):
        self.telegram_exporter.send_message(self.format(record))
