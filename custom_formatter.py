import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        output = "%(asctime)s [%(levelname)s] %(message)s"

        colors = {
            logging.DEBUG: "\x1b[38;20m" + output,
            logging.INFO: "\x1b[38;20m" + output,
            logging.WARNING: "\x1b[33;20m" + output,
            logging.ERROR: "\x1b[31;20m" + output,
            logging.CRITICAL: "\x1b[31;1m" + output
        }

        fmt = colors.get(record.levelno)
        formatter = logging.Formatter(fmt)

        return formatter.format(record)
