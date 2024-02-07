import logging


class CommonFormatter(logging.Formatter):
    def format(self, record):
        output = "%(asctime)s [%(levelname)s] %(message)s"

        colors = {
            logging.DEBUG: output,
            logging.INFO: output,
            logging.WARNING: output,
            logging.ERROR: output,
            logging.CRITICAL: output
        }

        fmt = colors.get(record.levelno)
        formatter = logging.Formatter(fmt)

        return formatter.format(record)
