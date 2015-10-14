from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import httplib2
import pytz
from apiclient import discovery
import oauth2client

from calendar_cli.operation.operation import Operation
from calendar_cli.util import omap, oget, ozip, universal_print
from calendar_cli.i18n import *


class SummaryOperation(Operation):
    def __init__(self, calendar_id, start_time, duration, credential_path):
        """
        :param calendar_id:
        :param start_time: datetime in tzinfo-aware
        :param duration: timedelta
        :param credential_path: path to the credential file
        """
        assert start_time.tzinfo is not None, 'start_time must be tzinfo-aware'

        Operation.__init__(
            self,
            ('calendar_id', calendar_id),
            ('start_time', start_time),
            ('duration', duration),
            ('credential_path', credential_path)
        )

    def _get_service(self):
        store = oauth2client.file.Storage(self.credential_path)
        credentials = store.get()

        assert credentials is not None and not credentials.invalid, '\n'.join([
            'Failed to load credential file: %s' % self.credential_path,
            'You need to create a credentials file by the following command:',
            '',
            '  calendar-cli setup client_secret.json',
            ''
        ])

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    @staticmethod
    def _get_event_time(event):
        return event['start'].get('dateTime'), event['end'].get('dateTime')

    @staticmethod
    def _extract_hour_minute(dt):
        # extract only HH:MM if the start datetime is set
        return dt[11:16]

    def _get_event_string(self, event):
        tm = omap('-'.join, ozip(*map(lambda x: omap(self._extract_hour_minute, x), self._get_event_time(event))))
        creator = event['creator'].get('displayName', event['creator']['email'])
        return '[%s] %s (%s)' % (oget(tm, MSG_ALL_DAY), event['summary'], creator)

    def run(self):
        service = self._get_service()

        limits = [self.start_time, self.start_time + self.duration]
        start_time, end_time = [x.astimezone(pytz.utc).isoformat() for x in limits]

        events_result = service.events().list(
            calendarId=self.calendar_id, timeMin=start_time, timeMax=end_time, maxResults=100, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = sorted(events_result.get('items', []), key=self._get_event_time)
        universal_print(sys.stdout, '\n'.join(self._get_event_string(e) for e in events) + '\n')
        return 0
