from __future__ import division, print_function, absolute_import, unicode_literals

from datetime import datetime, timedelta
import pytz
from mog_commons import unittest
from calendar_cli.operation import SummaryOperation
from calendar_cli.model import EventTime, Event
from calendar_cli.i18n import MSG_ALL_DAY, MSG_WEEK_DAY


class TestSummaryOperation(unittest.TestCase):

    def test_make_output(self):
        so1 = SummaryOperation('primary', datetime(2015, 10, 17, 0, 0, 0, 0, pytz.utc),
                               timedelta(days=3), 'dummy_path', '%D [%T] %S', None)
        so2 = SummaryOperation('primary', datetime(2015, 10, 17, 0, 0, 0, 0, pytz.utc),
                               timedelta(days=3), 'dummy_path', '%D [%T] %S', '')
        so3 = SummaryOperation('primary', datetime(2015, 10, 17, 0, 0, 0, 0, pytz.utc),
                               timedelta(days=3), 'dummy_path', '%D [%T] %S', '====')

        et1 = EventTime(True, datetime(2015, 10, 17, 9, 0, 0, 0, pytz.utc))
        et2 = EventTime(True, datetime(2015, 10, 17, 18, 0, 0, 0, pytz.utc))

        et3 = EventTime(False, datetime(2015, 10, 18, 0, 0, 0, 0, pytz.utc))
        et4 = EventTime(True, datetime(2015, 10, 18, 12, 15, 0, 0, pytz.utc))
        et5 = EventTime(True, datetime(2015, 10, 18, 12, 45, 0, 0, pytz.utc))

        et6 = EventTime(False, datetime(2015, 10, 19, 0, 0, 0, 0, pytz.utc))

        et7 = EventTime(False, datetime(2015, 10, 20, 0, 0, 0, 0, pytz.utc))

        ev1 = Event(et1, et2, 'Google I/O 2015', 'Foo Bar', 'foo@example.com')
        ev2 = Event(et3, et6, 'event 2', None, None)
        ev3 = Event(et4, et5, 'event 3', None, None)
        ev4 = Event(et6, et7, 'event 4', None, None)

        self.assertEqual(so1._make_output([ev1, ev2, ev3, ev4]), '\n'.join([
            '2015-10-17 %s [09:00-18:00] Google I/O 2015' % MSG_WEEK_DAY[5],
            '2015-10-18 %s [%s] event 2' % (MSG_WEEK_DAY[6], MSG_ALL_DAY),
            '2015-10-18 %s [12:15-12:45] event 3' % MSG_WEEK_DAY[6],
            '2015-10-19 %s [%s] event 4' % (MSG_WEEK_DAY[0], MSG_ALL_DAY),
        ]))
        self.assertEqual(so2._make_output([ev1, ev2, ev3, ev4]), '\n'.join([
            '2015-10-17 %s [09:00-18:00] Google I/O 2015' % MSG_WEEK_DAY[5],
            '',
            '2015-10-18 %s [%s] event 2' % (MSG_WEEK_DAY[6], MSG_ALL_DAY),
            '2015-10-18 %s [12:15-12:45] event 3' % MSG_WEEK_DAY[6],
            '',
            '2015-10-19 %s [%s] event 4' % (MSG_WEEK_DAY[0], MSG_ALL_DAY),
        ]))
        self.assertEqual(so3._make_output([ev1, ev2, ev3, ev4]), '\n'.join([
            '2015-10-17 %s [09:00-18:00] Google I/O 2015' % MSG_WEEK_DAY[5],
            '====',
            '2015-10-18 %s [%s] event 2' % (MSG_WEEK_DAY[6], MSG_ALL_DAY),
            '2015-10-18 %s [12:15-12:45] event 3' % MSG_WEEK_DAY[6],
            '====',
            '2015-10-19 %s [%s] event 4' % (MSG_WEEK_DAY[0], MSG_ALL_DAY),
        ]))
        self.assertEqual(so3._make_output([ev2, ev3]), '\n'.join([
            '2015-10-18 %s [%s] event 2' % (MSG_WEEK_DAY[6], MSG_ALL_DAY),
            '2015-10-18 %s [12:15-12:45] event 3' % MSG_WEEK_DAY[6],
        ]))
        self.assertEqual(so3._make_output([]), '')
