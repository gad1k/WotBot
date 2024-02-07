import sys
import logging

from telegram_agent import TelegramAgent


class TelegramHandler(logging.FileHandler):
    def __init__(self, token):
        logging.Handler.__init__(self)
        self.stream = sys.stdout

        self.telegram_agent = TelegramAgent(token)
        self.telegram_agent.retrieve_chat_id()


    def emit(self, record):
        self.telegram_agent.send_message(self.format(record))
