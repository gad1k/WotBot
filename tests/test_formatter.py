import logging

from datetime import datetime
from unittest import TestCase

from formatter import FileFormatter, StreamFormatter


class TestFileFormatter(TestCase):
    def test_format(self):
        file_formatter = FileFormatter()

        fmt_ts = "%Y-%m-%d %H:%M:%S"
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "Your gift for today: dummy_gift",
            "args": {},
            "exc_info": None
        }

        ar = file_formatter.format(logging.LogRecord(**attrs))
        actual_result = ar.split(",")[0] + " " + ar.split(" ", 2)[-1]
        er = datetime.today().strftime(fmt_ts)
        expected_result = er + " " + "[INFO] Your gift for today: dummy_gift"

        self.assertEqual(actual_result, expected_result)


class TestStreamFormatter(TestCase):
    def test_format(self):
        stream_formatter = StreamFormatter()

        fmt_ts = "%Y-%m-%d %H:%M:%S"
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "Your gift for today: dummy_gift",
            "args": {},
            "exc_info": None
        }

        ar = stream_formatter.format(logging.LogRecord(**attrs))
        actual_result = ar.split(",")[0] + " " + ar.split(" ", 2)[-1]
        er = datetime.today().strftime(fmt_ts)
        expected_result = "\x1b[38;20m" + er + " " + "[INFO] Your gift for today: dummy_gift\x1b[0m"

        self.assertEqual(actual_result, expected_result)
