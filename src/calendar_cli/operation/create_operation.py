from __future__ import division, print_function, absolute_import, unicode_literals

from calendar_cli.operation.operation import Operation
from calendar_cli.service import GoogleCalendarService
from calendar_cli.i18n import MSG_EVENT_CREATED
from mog_commons.io import print_safe


class CreateOperation(Operation):
    """Create an event to Google Calendar"""

    def __init__(self, calendar_id, event, credential_path):
        """
        :param calendar_id: string: calendar id
        :param event: calendar_cli.model.Event: event data to create
        :param credential_path: string: path to the credential file
        """
        Operation.__init__(
            self,
            ('calendar_id', calendar_id),
            ('event', event),
            ('credential_path', credential_path)
        )

    def run(self):
        service = GoogleCalendarService(self.credential_path)
        service.insert_event(self.calendar_id, self.event)
        print_safe(MSG_EVENT_CREATED % {'event': self.event.to_long_summary()})
