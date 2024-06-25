import logging


class FileFormatter(logging.Formatter):
    def format(self, record):
        output = "%(asctime)s [%(levelname)s] %(message)s"
        formatter = logging.Formatter(output)

        return formatter.format(record)


class StreamFormatter(logging.Formatter):
    def format(self, record):
        output = "%(asctime)s [%(levelname)s] %(message)s"

        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        colors = {
            logging.DEBUG: grey + output + reset,
            logging.INFO: grey + output + reset,
            logging.WARNING: yellow + output + reset,
            logging.ERROR: red + output + reset,
            logging.CRITICAL: bold_red + output + reset
        }

        fmt = colors.get(record.levelno)
        formatter = logging.Formatter(fmt)

        return formatter.format(record)
