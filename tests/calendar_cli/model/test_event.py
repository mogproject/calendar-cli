# encoding: utf-8
from __future__ import division, print_function, absolute_import, unicode_literals

from datetime import datetime
import pytz
from mog_commons import unittest
from calendar_cli.model import EventTime, Event
from calendar_cli.i18n import MSG_ALL_DAY, MSG_WEEK_DAY


class TestEventTime(unittest.TestCase):
    tz_tokyo = pytz.timezone('Asia/Tokyo')

    d0 = datetime(2015, 10, 17, 0, 0, 0, 0, pytz.timezone('Asia/Tokyo'))
    d1 = datetime(2015, 10, 18, 0, 0, 0, 0, pytz.timezone('Asia/Tokyo'))
    d2 = datetime(2015, 10, 17, 0, 0, 0, 0, pytz.utc)
    d3 = datetime(2016, 10, 17, 0, 0, 0, 0, pytz.utc)
    d4 = datetime(2015, 10, 17, 12, 34, 56, 0, pytz.timezone('Asia/Tokyo'))
    d5 = datetime(2015, 10, 18, 12, 34, 56, 0, pytz.timezone('Asia/Tokyo'))
    d6 = datetime(2015, 10, 17, 3, 34, 56, 0, pytz.utc)
    d7 = datetime(2015, 10, 17, 3, 34, 57, 0, pytz.utc)

    def test_init(self):
        t = EventTime(False, self.d1)
        self.assertFalse(t.has_time)
        self.assertEqual(t.datetime_tz, self.d1)
        t = EventTime(True, self.d5)
        self.assertTrue(t.has_time)
        self.assertEqual(t.datetime_tz, self.d5)

    def test_init_error(self):
        self.assertRaisesRegexp(AssertionError, 'datetime_tz must be timezone-aware',
                                EventTime, True, datetime(2015, 10, 17, 12, 34, 56))

    def test_cmp(self):
        ts1 = [EventTime(False, t) for t in [self.d0, self.d1, self.d2, self.d3]]
        ts2 = [EventTime(True, t) for t in [self.d4, self.d5, self.d6, self.d7]]
        ts = ts1 + ts2
        self.assertEqual(sorted(ts), [ts[0], ts[2], ts[1], ts[3], ts[6], ts[4], ts[7], ts[5]])

    def test_to_short_summary(self):
        self.assertEqual(EventTime(False, self.d0).to_short_summary(), None)
        self.assertEqual(EventTime(False, self.d2).to_short_summary(), None)
        self.assertEqual(EventTime(True, self.d4).to_short_summary(), '12:34')
        self.assertEqual(EventTime(True, self.d6).to_short_summary(), '03:34')

    def test_to_long_summary(self):
        self.assertEqual(EventTime(False, self.d0).to_long_summary(), '2015-10-17 %s' % MSG_WEEK_DAY[5])
        self.assertEqual(EventTime(False, self.d2).to_long_summary(), '2015-10-17 %s' % MSG_WEEK_DAY[5])
        self.assertEqual(EventTime(True, self.d4).to_long_summary(), '2015-10-17 %s' % MSG_WEEK_DAY[5])
        self.assertEqual(EventTime(True, self.d6).to_long_summary(), '2015-10-17 %s' % MSG_WEEK_DAY[5])

    def test_to_dict(self):
        self.assertEqual(EventTime(False, self.d0).to_dict(),
                         {'date': '2015-10-17', 'timeZone': 'Asia/Tokyo'})
        self.assertEqual(EventTime(False, self.d2).to_dict(),
                         {'date': '2015-10-17', 'timeZone': 'UTC'})
        self.assertEqual(EventTime(True, self.d4).to_dict(),
                         {'dateTime': '2015-10-17T12:34:56+09:00', 'timeZone': 'Asia/Tokyo'})
        self.assertEqual(EventTime(True, self.d6).to_dict(),
                         {'dateTime': '2015-10-17T03:34:56+00:00', 'timeZone': 'UTC'})

    def test_parse_dict(self):
        self.assertEqual(EventTime.parse_dict({'date': '2015-10-17'}, 'Asia/Tokyo'),
                         EventTime(False, datetime(2015, 10, 17, 0, 0, 0, 0, self.tz_tokyo)))
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00+09:00'}, 'Asia/Tokyo'),
                         EventTime(True, datetime(2015, 10, 1, 10, 30, 0, 0, self.tz_tokyo)))
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00+09:00', 'timeZone': 'Asia/Tokyo'},
                                              'Asia/Tokyo'),
                         EventTime(True, datetime(2015, 10, 1, 10, 30, 0, 0, self.tz_tokyo)))
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00Z'}, 'Asia/Tokyo'),
                         EventTime(True, datetime(2015, 10, 1, 19, 30, 0, 0, self.tz_tokyo)))
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00-04:00'}, 'Asia/Tokyo'),
                         EventTime(True, datetime(2015, 10, 1, 23, 30, 0, 0, self.tz_tokyo)))

        # When the timezone doesn't match the timeZone field, ignore timeZone.
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00-04:00'}, 'UTC'),
                         EventTime(True, datetime(2015, 10, 1, 14, 30, 0, 0, pytz.utc)))

        # When the timezone is missing in dateTime field, use timeZone filed to parse.
        self.assertEqual(EventTime.parse_dict({'dateTime': '2015-10-01T10:30:00', 'timeZone': 'Asia/Tokyo'}, 'UTC'),
                         EventTime(True, datetime(2015, 10, 1, 1, 30, 0, 0, pytz.utc)))


class TestEvent(unittest.TestCase):
    tz_la = pytz.timezone('America/Los_Angeles')
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    t0 = EventTime(True, tz_la.localize(datetime(2015, 5, 28, 9, 0, 0, 0)))
    t1 = EventTime(True, tz_la.localize(datetime(2015, 5, 28, 17, 0, 0, 0)))
    t2 = EventTime(False, tz_tokyo.localize(datetime(2015, 10, 17, 0, 0, 0, 0)))
    t3 = EventTime(False, tz_tokyo.localize(datetime(2015, 10, 18, 0, 0, 0, 0)))
    t4 = EventTime(False, datetime(2015, 10, 18, 0, 0, 0, 0, pytz.utc))

    e0 = Event(t0, t1, 'Google I/O 2015', 'Foo Bar', 'foo@example.com')
    e1 = Event(t2, t3, 'あいうえお', None, None)
    e2 = Event(t2, t3, 'あいうえお', None, 'foo@example.com')
    e3 = Event(t0, t1, 'Google I/O 2016', 'Foo Bar', 'foo@example.com', 'Mountain View')

    def test_init(self):
        self.assertEqual(self.e0.start_time, self.t0)
        self.assertEqual(self.e0.end_time, self.t1)
        self.assertEqual(self.e0.summary, 'Google I/O 2015')
        self.assertEqual(self.e0.creator_name, 'Foo Bar')
        self.assertEqual(self.e0.creator_email, 'foo@example.com')

        self.assertEqual(self.e1.start_time, self.t2)
        self.assertEqual(self.e1.end_time, self.t3)
        self.assertEqual(self.e1.summary, 'あいうえお')
        self.assertEqual(self.e1.creator_name, None)
        self.assertEqual(self.e1.creator_email, None)

    def test_init_error(self):
        """todo"""

    def test_to_format(self):
        self.assertEqual(self.e0.to_format('[%T] %S%L%C'), '[09:00-17:00] Google I/O 2015 (Foo Bar)')
        self.assertEqual(self.e1.to_format('[%T] %S%L%C'), '[%s] あいうえお' % MSG_ALL_DAY)
        self.assertEqual(self.e2.to_format('[%T] %S%L%C'), '[%s] あいうえお (foo@example.com)' % MSG_ALL_DAY)
        self.assertEqual(self.e3.to_format('[%T] %S%L%C'), '[09:00-17:00] Google I/O 2016 @Mountain View (Foo Bar)')

    def test_to_long_summary(self):
        self.assertEqual(self.e0.to_long_summary(), '2015-05-28 %s [09:00-17:00] Google I/O 2015' % MSG_WEEK_DAY[3])
        self.assertEqual(self.e1.to_long_summary(), '2015-10-17 %s [%s] あいうえお' % (MSG_WEEK_DAY[5], MSG_ALL_DAY))
        self.assertEqual(self.e2.to_long_summary(), '2015-10-17 %s [%s] あいうえお' % (MSG_WEEK_DAY[5], MSG_ALL_DAY))

    def test_to_dict(self):
        self.assertEqual(self.e0.to_dict(), {
            'summary': 'Google I/O 2015',
            'start': {'dateTime': '2015-05-28T09:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'end': {'dateTime': '2015-05-28T17:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'creator': {'displayName': 'Foo Bar', 'email': 'foo@example.com', },
        })
        self.assertEqual(self.e1.to_dict(), {
            'summary': 'あいうえお',
            'start': {'date': '2015-10-17', 'timeZone': 'Asia/Tokyo'},
            'end': {'date': '2015-10-18', 'timeZone': 'Asia/Tokyo'},
        })
        self.assertEqual(self.e2.to_dict(), {
            'summary': 'あいうえお',
            'start': {'date': '2015-10-17', 'timeZone': 'Asia/Tokyo'},
            'end': {'date': '2015-10-18', 'timeZone': 'Asia/Tokyo'},
            'creator': {'email': 'foo@example.com'},
        })

    def test_parse_dict(self):
        self.assertEqual(Event.parse_dict({
            'summary': 'Google I/O 2015',
            'start': {'dateTime': '2015-05-28T09:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'end': {'dateTime': '2015-05-28T17:00:00-07:00', 'timeZone': 'America/Los_Angeles'},
            'creator': {'displayName': 'Foo Bar', 'email': 'foo@example.com', },
        }, 'America/Los_Angeles'), self.e0)
        self.assertEqual(Event.parse_dict({
            'summary': 'あいうえお',
            'start': {'date': '2015-10-17'},
            'end': {'date': '2015-10-18'},
        }, 'Asia/Tokyo'), self.e1)

        self.assertEqual(Event.parse_dict({
            'summary': 'あいうえお',
            'start': {'date': '2015-10-17'},
            'end': {'date': '2015-10-18'},
            'creator': {'email': 'foo@example.com'},
        }, 'Asia/Tokyo'), self.e2)
