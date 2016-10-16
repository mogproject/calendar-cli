from __future__ import division, print_function, absolute_import, unicode_literals

import itertools
from calendar_cli.operation.operation import Operation
from calendar_cli.service import GoogleCalendarService
from mog_commons.functional import omap
from mog_commons.io import print_safe


class SummaryOperation(Operation):
    """Print summary of Google Calender"""

    def __init__(self, calendar_id, start_time, duration, credential_path, format, separator):
        """
        :param calendar_id: string: calendar id
        :param start_time: datetime in tzinfo-aware
        :param duration: timedelta
        :param credential_path: string: path to the credential file
        :param format: string: format string
        :param separator: string: date separator string
        """
        assert start_time.tzinfo is not None, 'start_time must be tzinfo-aware'

        Operation.__init__(
            self,
            ('calendar_id', calendar_id),
            ('start_time', start_time),
            ('duration', duration),
            ('credential_path', credential_path),
            ('format', format),
            ('separator', separator)
        )

    def _make_output(self, events):
        """Make the output string from an event list."""

        # group by event date
        f = lambda e: e.start_time.to_date()
        evs = ['\n'.join(e.to_format(self.format) for e in g) for k, g in itertools.groupby(events, f)]
        sep = (omap(lambda s: '\n' + s, self.separator) or '') + '\n'

        # make the result string
        return sep.join(evs)

    def run(self):
        # fetch events
        service = GoogleCalendarService(self.credential_path)
        events = service.list_events(self.calendar_id, self.start_time, self.start_time + self.duration)

        # print the result
        print_safe(self._make_output(events))
        return 0
