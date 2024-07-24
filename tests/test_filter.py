import logging

from unittest import TestCase

from modules.filter import CommonFilter, StreamFilter


class TestCommonFilter(TestCase):
    def setUp(self):
        self.common_filter = CommonFilter()


    def test_filter_level(self):
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "Your gift for today: dummy_gift",
            "args": {},
            "exc_info": None
        }

        self.assertTrue(self.common_filter.filter(logging.LogRecord(**attrs)))


    def test_filter_msg(self):
        attrs = {
            "name": "dummy_name",
            "level": 40,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        self.assertTrue(self.common_filter.filter(logging.LogRecord(**attrs)))


    def test_filter_none(self):
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        self.assertFalse(self.common_filter.filter(logging.LogRecord(**attrs)))


class TestStreamFilter(TestCase):
    def setUp(self):
        self.stream_filter = StreamFilter()


    def test_filter_module(self):
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "wot_bot",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        self.assertTrue(self.stream_filter.filter(logging.LogRecord(**attrs)))


    def test_filter_none(self):
        attrs = {
            "name": "dummy_name",
            "level": 20,
            "pathname": "dummy_path",
            "lineno": 2,
            "msg": "dummy_message",
            "args": {},
            "exc_info": None
        }

        self.assertFalse(self.stream_filter.filter(logging.LogRecord(**attrs)))
