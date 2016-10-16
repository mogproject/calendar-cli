from __future__ import division, print_function, absolute_import, unicode_literals

from dateutil import parser
import pytz
from mog_commons.case_class import CaseClass
from mog_commons.functional import oget, omap, ozip
from calendar_cli.i18n import MSG_ALL_DAY, MSG_WEEK_DAY


class EventTime(CaseClass):
    def __init__(self, has_time, datetime_tz):
        """
        :param has_time: bool: False if the all-day event
        :param datetime_tz: datetime: timezone-aware datetime
        """
        assert datetime_tz.tzinfo is not None, 'datetime_tz must be timezone-aware'
        CaseClass.__init__(self, ('has_time', has_time), ('datetime_tz', datetime_tz))

    def to_short_summary(self):
        return self.datetime_tz.strftime('%H:%M') if self.has_time else None

    def to_long_summary(self):
        return self.datetime_tz.strftime('%Y-%m-%d ') + MSG_WEEK_DAY[self.datetime_tz.weekday()]

    def to_dict(self):
        if self.has_time:
            d = {'dateTime': self.datetime_tz.isoformat()}
        else:
            d = {'date': self.datetime_tz.date().isoformat()}
        d.update(oget(omap(lambda tz: {'timeZone': str(tz)}, self.datetime_tz.tzinfo), {}))
        return d

    def to_date(self):
        return self.datetime_tz.date()

    @staticmethod
    def parse_dict(d, default_timezone):
        tz = pytz.timezone(default_timezone)  # always read as default timezone
        if 'dateTime' in d:
            dt = parser.parse(d['dateTime'])  # parse as tz-aware datetime
            if dt.tzinfo is None and 'timeZone' in d:
                dt = pytz.timezone(d['timeZone']).localize(dt)
            return EventTime(True, dt.astimezone(tz))
        else:
            dt = parser.parse(d['date'])
            dt = tz.localize(dt)
            return EventTime(False, dt)


class Event(CaseClass):
    def __init__(self,
                 start_time,
                 end_time,
                 summary,
                 creator_name=None,
                 creator_email=None,
                 location=None):
        """
        :param start_time: EventTime:
        :param end_time: EventTime:
        :param summary: unicode:
        :param creator_name: unicode:
        :param creator_email: unicode:
        :param location: unicode:
        """
        assert isinstance(start_time, EventTime)
        assert isinstance(end_time, EventTime)
        assert start_time.has_time == end_time.has_time
        assert start_time <= end_time

        CaseClass.__init__(self,
                           ('start_time', start_time),
                           ('end_time', end_time),
                           ('summary', summary),
                           ('creator_name', creator_name),
                           ('creator_email', creator_email),
                           ('location', location)
                           )

    def str_time_range(self):
        s = ozip(self.start_time.to_short_summary(), self.end_time.to_short_summary())
        return oget(omap('-'.join, s), MSG_ALL_DAY)

    def str_creator(self):
        return omap(lambda s: '%s' % s, oget(self.creator_name, self.creator_email))

    def to_long_summary(self):
        """
        :return: e.g. '2015-05-28 Wed [ALLDAY] Google I/O 2015'
                      '2015-05-28 Wed [10:30-11:00] Stand-up meeting
        """
        return self.to_format('%D [%T] %S')

    def to_format(self, format_):
        return (
            format_
            .replace('%D', self.start_time.to_long_summary())
            .replace('%T', self.str_time_range())
            .replace('%S', self.summary)
            .replace('%C', oget(omap(lambda s: ' (%s)' % s, self.str_creator()), ''))
            .replace('%L', oget(omap(lambda s: ' @%s' % s, self.location), ''))
        )

    def to_dict(self):
        r = {'summary': self.summary, 'start': self.start_time.to_dict(), 'end': self.end_time.to_dict()}

        d = {}
        omap(lambda x: d.update({'displayName': x}), self.creator_name)
        omap(lambda x: d.update({'email': x}), self.creator_email)
        if d:
            r.update({'creator': d})

        omap(lambda x: r.update({'location': x}), self.location)
        return r

    @staticmethod
    def parse_dict(d, default_timezone):
        return Event(EventTime.parse_dict(d['start'], default_timezone),
                     EventTime.parse_dict(d['end'], default_timezone),
                     d['summary'],
                     omap(lambda x: x.get('displayName'), (d.get('creator'))),
                     omap(lambda x: x.get('email'), (d.get('creator'))),
                     d.get('location'))
