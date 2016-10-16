# encoding: utf-8
from __future__ import division, print_function, absolute_import, unicode_literals

import six
from datetime import datetime, timedelta
from tzlocal import get_localzone
from mog_commons import unittest
from calendar_cli.model import EventTime, Event
from calendar_cli.setting.setting import Setting
from calendar_cli.operation import *


class TestSetting(unittest.TestCase):

    @staticmethod
    def _localize(year, month, day, hour, minute):
        return get_localzone().localize(datetime(year, month, day, hour, minute))

    def test_parse_args(self):
        # create
        a0 = ['calendar-cli', 'create', '--date', '20151018', '--start', '1030', '--end', '1100',
              'あいう'.encode('utf-8'), 'えお'.encode('utf-8')]
        s0 = Setting().parse_args(a0)

        self.assertIsInstance(s0.operation, CreateOperation)
        self.assertEqual(s0.operation.calendar_id, 'primary')
        self.assertEqual(s0.operation.event, Event(
            EventTime(True, self._localize(2015, 10, 18, 10, 30)),
            EventTime(True, self._localize(2015, 10, 18, 11, 00)),
            'あいう えお'
        ))

        # summary
        t = datetime.now()
        today = get_localzone().localize(datetime(t.year, t.month, t.day))

        a = ['calendar-cli']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today)
        self.assertEqual(s.operation.duration, timedelta(days=1))
        self.assertEqual(s.operation.format, '[%T] %S%L%C')

        a = ['calendar-cli', '--days', '0']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today)
        self.assertEqual(s.operation.duration, timedelta(days=1))
        self.assertEqual(s.operation.format, '[%T] %S%L%C')

        a = ['calendar-cli', '--days', '1']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today)
        self.assertEqual(s.operation.duration, timedelta(days=2))
        self.assertEqual(s.operation.format, '%D [%T] %S%L%C')

        a = ['calendar-cli', '--days', '6']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today)
        self.assertEqual(s.operation.duration, timedelta(days=7))
        self.assertEqual(s.operation.format, '%D [%T] %S%L%C')

        a = ['calendar-cli', '--days', '6', '--format', '%D %S']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today)
        self.assertEqual(s.operation.duration, timedelta(days=7))
        self.assertEqual(s.operation.format, '%D %S')

        a = ['calendar-cli', '--days', '-1']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, today - timedelta(days=1))
        self.assertEqual(s.operation.duration, timedelta(days=2))
        self.assertEqual(s.operation.format, '%D [%T] %S%L%C')

        a = ['calendar-cli', '--date', '20151018']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, self._localize(2015, 10, 18, 0, 0))
        self.assertEqual(s.operation.duration, timedelta(days=1))
        self.assertEqual(s.operation.format, '[%T] %S%L%C')

        a = ['calendar-cli', '--date', '20151018', '--days', '-3', '--format', '%S']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SummaryOperation)
        self.assertEqual(s.operation.calendar_id, 'primary')
        self.assertEqual(s.operation.start_time, self._localize(2015, 10, 15, 0, 0))
        self.assertEqual(s.operation.duration, timedelta(days=4))
        self.assertEqual(s.operation.format, '%S')

        # setup
        a = ['calendar-cli', 'setup', 'client_secret.json']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SetupOperation)
        self.assertEqual(s.operation.secret_path, 'client_secret.json')
        self.assertEqual(s.operation.read_only, False)
        self.assertEqual(s.operation.no_browser, False)

        a = ['calendar-cli', 'setup', 'client_secret.json', '--read-only', '--no-browser']
        s = Setting().parse_args(a)

        self.assertIsInstance(s.operation, SetupOperation)
        self.assertEqual(s.operation.secret_path, 'client_secret.json')
        self.assertEqual(s.operation.read_only, True)
        self.assertEqual(s.operation.no_browser, True)

    def test_parse_time_range(self):
        now = self._localize(2015, 10, 19, 9, 30)

        def f(has_time, start_year, start_month, start_day, start_hour, start_minute,
              end_year, end_month, end_day, end_hour, end_minute, *args):
            self.assertEqual(
                Setting._parse_time_range(*args, now=now),
                (EventTime(has_time, self._localize(start_year, start_month, start_day, start_hour, start_minute)),
                 EventTime(has_time, self._localize(end_year, end_month, end_day, end_hour, end_minute))))

        # without --date option
        f(True, 2015, 10, 19, 10, 0, 2015, 10, 19, 10, 15, None, '1000', None)
        f(True, 2015, 10, 20, 9, 29, 2015, 10, 20, 9, 44, None, '0929', None)
        f(True, 2015, 10, 19, 9, 30, 2015, 10, 19, 9, 45, None, '0930', None)
        f(True, 2015, 10, 20, 0, 0, 2015, 10, 20, 0, 15, None, '0000', None)
        f(True, 2015, 10, 19, 23, 59, 2015, 10, 20, 0, 14, None, '2359', None)

        f(True, 2015, 10, 19, 10, 0, 2015, 10, 19, 10, 15, None, '10:00', None)
        f(True, 2015, 10, 19, 10, 0, 2015, 10, 19, 10, 15, None, '10:0', None)
        f(True, 2015, 10, 20, 9, 5, 2015, 10, 20, 9, 20, None, '9:5', None)
        f(True, 2015, 10, 20, 9, 5, 2015, 10, 20, 9, 20, None, '9:05', None)

        f(True, 2015, 10, 20, 0, 0, 2015, 10, 20, 0, 0, None, '0000', '0000')
        f(True, 2015, 10, 20, 0, 0, 2015, 10, 20, 0, 1, None, '0000', '0001')
        f(True, 2015, 10, 20, 0, 0, 2015, 10, 20, 23, 59, None, '0000', '2359')
        f(True, 2015, 10, 20, 0, 1, 2015, 10, 21, 0, 0, None, '0001', '0:0')
        f(True, 2015, 10, 19, 23, 59, 2015, 10, 20, 0, 0, None, '23:59', '0:0')
        f(True, 2015, 10, 19, 23, 59, 2015, 10, 20, 23, 58, None, '23:59', '23:58')
        f(True, 2015, 10, 19, 23, 59, 2015, 10, 19, 23, 59, None, '23:59', '23:59')
        f(True, 2015, 10, 19, 23, 55, 2015, 10, 20, 0, 5, None, '23:55', '00:5')

        # with --date option
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '20140102', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014-1-2', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014-1-02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014-01-2', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014-01-02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014/1/2', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014/1/02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014/01/2', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014/01/02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014/01-02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '2014-01/02', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '1-2-2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '1-02-2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01-2-2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01-02-2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '1/2/2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '1/02/2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01/2/2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01/02/2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01-02/2014', None, None)
        f(False, 2014, 1, 2, 0, 0, 2014, 1, 2, 0, 0, '01/02-2014', None, None)

        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '1-2', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '1-02', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '01-2', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '01-02', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '1/2', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '1/02', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '01/2', None, None)
        f(False, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 0, '01/02', None, None)

        f(True, 2015, 1, 2, 0, 0, 2015, 1, 2, 0, 15, '01/02', '0000', None)
        f(True, 2015, 12, 31, 23, 59, 2016, 1, 1, 0, 14, '12/31', '2359', None)
        f(True, 2015, 1, 2, 0, 0, 2015, 1, 2, 23, 59, '01/02', '0000', '2359')
        f(True, 2015, 12, 31, 23, 59, 2016, 1, 1, 0, 0, '12/31', '2359', '0000')
        f(True, 2016, 2, 29, 10, 0, 2016, 3, 1, 9, 0, '2016/2/29', '10:00', '9:0')

    def test_parse_time_range_error(self):
        now = self._localize(2015, 10, 19, 9, 30)

        def f(expect_regexp, *args):
            self.assertRaisesRegexp(ValueError, expect_regexp, Setting._parse_time_range, *args, now=now)

        def g(expect_regexp, *args):
            with self.assertRaises(ValueError) as cm:
                Setting._parse_time_range(*args, now=now)
            if six.PY2:
                self.assertRegexpMatches(cm.exception.message, expect_regexp)
            else:
                self.assertRegex(str(cm.exception), expect_regexp)

        f(r'Failed to create event: --date or --start options are missing\.', None, None, None)
        f(r'Failed to create event: --date or --start options are missing\.', None, None, '1100')
        f(r'Failed to create event: --date option with --end is set but --start is missing\.', '1/1', None, '1100')
        f(r'Failed to parse --date option:', 'a', None, None)
        f(r'Failed to parse --start or --end option:', None, 'a', None)
        f(r'Failed to parse --date option:', '2015-02-29', None, None)
        f(r'Failed to parse --start or --end option:', None, '900', None)

        g(r'Failed to parse --date option:', 'あ', None, None)
        g(r'Failed to parse --start or --end option:', None, 'あ', None)
