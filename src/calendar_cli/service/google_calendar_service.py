from __future__ import division, print_function, absolute_import, unicode_literals

import pytz
import httplib2
from apiclient import discovery
import oauth2client.file
from calendar_cli.model import Event

MAX_RESULTS = 100


class GoogleCalendarService(object):
    def __init__(self, credential_path):
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()

        assert credentials is not None and not credentials.invalid, '\n'.join([
            'Failed to load credential file: %s' % credential_path,
            'You need to create a credentials file by the following command:',
            '',
            '  calendar-cli setup client_secret.json',
            ''
        ])

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        self._service = service

    def list_events(self, calendar_id, time_min, time_max):
        """
        :return: list[Event]: event list sorted by startTime and endTime (all-day events come first)
        """
        params = {
            'calendarId': calendar_id,
            'timeMin': time_min.astimezone(pytz.utc).isoformat(),
            'timeMax': time_max.astimezone(pytz.utc).isoformat(),
            'maxResults': MAX_RESULTS,
            'singleEvents': True,
            'orderBy': 'startTime'
        }
        events_result = self._service.events().list(**params).execute()
        return sorted(Event.parse_dict(d, events_result['timeZone']) for d in events_result.get('items', []))

    def insert_event(self, calendar_id, event):
        """
        :param calendar_id: string:
        :param event: Event:
        :return: string: event id
        """
        ret = self._service.events().insert(calendarId=calendar_id, body=event.to_dict()).execute()
        return ret['id']
