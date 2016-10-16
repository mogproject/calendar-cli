from __future__ import division, print_function, absolute_import, unicode_literals

import re
from datetime import datetime, timedelta
from tzlocal import get_localzone
from calendar_cli.model import EventTime, Event
from calendar_cli.operation import HelpOperation, SummaryOperation, CreateOperation, SetupOperation
from calendar_cli.setting import arg_parser
from mog_commons.case_class import CaseClass
from mog_commons.functional import oget
from mog_commons.string import to_unicode


class Setting(CaseClass):
    """Manages all settings."""

    DEFAULT_CREATE_DURATION = timedelta(minutes=15)

    def __init__(self, operation=None, now=None, debug=None):
        CaseClass.__init__(self,
                           ('operation', operation),
                           ('now', now or get_localzone().localize(datetime.now())),
                           ('debug', debug)
                           )

    @staticmethod
    def _parse_date(s, now):
        if s is None:
            return None
        try:
            # YYYYmmdd
            if re.compile(r"""^[0-9]{8}$""").match(s):
                return datetime.strptime(s, '%Y%m%d').date()

            # mm/dd or mm-dd (complete with the current year)
            m = re.compile(r"""^([0-9]{1,2})[/-]([0-9]{1,2})$""").match(s)
            if m:
                mm, dd = m.group(1), m.group(2)
                return datetime.strptime(mm.rjust(2, '0') + dd.rjust(2, '0'), '%m%d').date().replace(year=now.year)

            # YYYY/MM/DD or YYYY-MM-DD
            m = re.compile(r"""^([0-9]{4})[/-]([0-9]{1,2})[/-]([0-9]{1,2})$""").match(s)
            if m:
                yyyy, mm, dd = m.group(1), m.group(2), m.group(3)
                return datetime.strptime(yyyy + mm.rjust(2, '0') + dd.rjust(2, '0'), '%Y%m%d').date()

            # MM/DD/YYYY or MM-DD-YYYY
            m = re.compile(r"""^([0-9]{1,2})[/-]([0-9]{1,2})[/-]([0-9]{4})$""").match(s)
            if m:
                mm, dd, yyyy = m.group(1), m.group(2), m.group(3)
                return datetime.strptime(yyyy + mm.rjust(2, '0') + dd.rjust(2, '0'), '%Y%m%d').date()

            raise ValueError()
        except ValueError:
            raise ValueError('Failed to parse --date option: %s' % s)

    @staticmethod
    def _parse_time(s):
        if s is None:
            return None
        try:
            # HHMM
            if re.compile(r"""^[0-9]{4}$""").match(s):
                return datetime.strptime(s, '%H%M').time()

            # HH:MM
            m = re.compile(r"""^([0-9]{1,2}):([0-9]{1,2})$""").match(s)
            if m:
                hh, mm = m.group(1), m.group(2)
                return datetime.strptime(hh.rjust(2, '0') + mm.rjust(2, '0'), '%H%M').time()

            raise ValueError()
        except ValueError:
            raise ValueError('Failed to parse --start or --end option: %s' % s)

    @classmethod
    def _parse_time_range(cls, date, start_time, end_time, now):
        parsed_date = cls._parse_date(date, now)
        parsed_start = cls._parse_time(start_time)
        parsed_end = cls._parse_time(end_time)

        if parsed_date is None:
            if parsed_start is None:
                raise ValueError('Failed to create event: --date or --start options are missing.')
            # set date today or tomorrow
            dt = now.date()
            if (parsed_start.hour, parsed_start.minute) < (now.hour, now.minute):
                dt += timedelta(days=1)
        else:
            if parsed_start is None:
                if parsed_end is not None:
                    raise ValueError('Failed to create event: --date option with --end is set but --start is missing.')
                # all-day event
                t = get_localzone().localize(datetime(parsed_date.year, parsed_date.month, parsed_date.day))
                return EventTime(False, t), EventTime(False, t)
            dt = parsed_date

        # set start and end event time
        start = get_localzone().localize(datetime.combine(dt, parsed_start))

        if parsed_end is None:
            end = start + cls.DEFAULT_CREATE_DURATION
        else:
            end = get_localzone().localize(datetime.combine(dt, parsed_end))
            if parsed_start > parsed_end:
                end += timedelta(days=1)
        return EventTime(True, start), EventTime(True, end)

    def parse_args(self, argv):
        assert self.now is not None

        # decode all args as utf-8
        option, args = arg_parser.parser.parse_args([to_unicode(a, errors='ignore') for a in argv[1:]])

        try:
            if not args:
                # summary
                dt = oget(self._parse_date(option.date, self.now), self.now.date())
                start_time = get_localzone().localize(datetime(dt.year, dt.month, dt.day))

                fmt = (option.format or
                       (arg_parser.DEFAULT_FORMAT if option.days == 0 else arg_parser.DEFAULT_FORMAT_DAYS))

                if option.days == 0:
                    # show events on one day
                    duration = timedelta(days=1)
                elif option.days < 0:
                    # show events from past several days
                    duration = timedelta(days=-option.days + 1)
                    start_time -= timedelta(days=-option.days)
                else:
                    # show events from several days from today
                    duration = timedelta(days=option.days + 1)

                operation = SummaryOperation(option.calendar, start_time, duration,
                                             option.credential, fmt, option.separator)
            elif args[0] == 'setup' and len(args) == 2:
                # setup
                operation = SetupOperation(args[1], option.credential, option.read_only, option.no_browser)
            elif args[0] == 'create' and len(args) >= 2:
                # create
                summary = ' '.join(args[1:])
                start, end = self._parse_time_range(option.date, option.start_time, option.end_time, self.now)
                ev = Event(start, end, summary, location=option.location)
                operation = CreateOperation(option.calendar, ev, option.credential)
            else:
                # help
                operation = HelpOperation()
        except Exception as e:
            # parse error
            operation = HelpOperation(e)
            if option.debug:
                import traceback
                traceback.print_exc()
                print()

        return self.copy(operation=operation, debug=option.debug)
