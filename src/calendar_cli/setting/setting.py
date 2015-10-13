from __future__ import division, print_function, absolute_import, unicode_literals

from datetime import date, datetime, timedelta
from dateutil.tz import tzlocal
from calendar_cli.operation import HelpOperation, SetupOperation, SummaryOperation
from calendar_cli.setting import arg_parser
from calendar_cli.util import CaseClass


class Setting(CaseClass):
    """Manages all settings."""

    DEFAULT_DURATION = timedelta(days=1)

    def __init__(self, operation=None):
        CaseClass.__init__(self, ('operation', operation))

    def copy(self, **args):
        d = self.values()
        d.update(args)
        return Setting(**d)

    def parse_args(self, argv):
        option, args = arg_parser.parser.parse_args(argv[1:])

        if not args:
            # summary
            calendar_id = option.calendar
            dt = date.today() if option.date is None else datetime.strptime(option.date, '%Y%m%d').date()
            start_time = datetime(dt.year, dt.month, dt.day, tzinfo=tzlocal())

            operation = SummaryOperation(calendar_id, start_time, Setting.DEFAULT_DURATION, option.credential)
        elif args[0] == 'setup' and len(args) == 2:
            # setup
            operation = SetupOperation(args[1], option.credential)
        else:
            # help
            operation = HelpOperation()

        return Setting(operation)
