from __future__ import division, print_function, absolute_import, unicode_literals

import os
from optparse import OptionParser

VERSION = 'calendar-cli %s' % __import__('calendar_cli').__version__

USAGE = """
  %prog [options]
                        Print a summary of events on the calendar.

  %prog setup <secret_path> [--read-only --no-browser --credential <credential_path>]
                        Generate a credentials file from the client secret.

  %prog create [--date <YYYYMMDD> --start <HHMM> --end <HHMM> --location <location>
                --credential <credential_path>] <summary>
                        Create an event onto the calendar.
"""


DEFAULT_CREDENTIAL_PATH = os.path.join(os.path.expanduser('~'), '.credentials', 'calendar-cli.json')
DEFAULT_FORMAT = '[%T] %S%L%C'
DEFAULT_FORMAT_DAYS = '%D [%T] %S%L%C'


def _get_parser():
    p = OptionParser(usage=USAGE, version=VERSION)
    p.add_option(
        '--calendar', dest='calendar', default='primary', type='string', metavar='CALENDAR',
        help='set calendar id to CALENDAR (default:primary)'
    )
    p.add_option(
        '--date', dest='date', default=None, type='string', metavar='YYYYMMDD',
        help='set date to YYYYMMDD in the summary/create command (default:today)'
    )
    p.add_option(
        '--days', dest='days', default=0, type=int, metavar='N',
        help=' '.join([
            'show events from the next N days in the summary command (default:0)',
            'If you set a negative number(-N), events from past N days will be shown.'
        ])
    )
    p.add_option(
        '--credential', dest='credential', default=DEFAULT_CREDENTIAL_PATH, type='string', metavar='CREDENTIAL',
        help='set credential path to CREDENTIAL (default:%s)' % DEFAULT_CREDENTIAL_PATH
    )
    p.add_option(
        '--read-only', dest='read_only', action='store_true', default=False,
        help='create a read-only credential file in the setup command (default: False)'
    )
    p.add_option(
        '--no-browser', dest='no_browser', action='store_true', default=False,
        help='create a credential file without launching a web browser in the setup command (default: False)'
    )
    p.add_option(
        '--start', dest='start_time', default=None, type='string', metavar='HHMM',
        help='set start time in the create command'
    )
    p.add_option(
        '--end', dest='end_time', default=None, type='string', metavar='HHMM',
        help='set end time in the create command'
    )
    p.add_option(
        '--location', dest='location', default=None, type='string', metavar='LOCATION',
        help='set location to LOCATION in the create command'
    )
    p.add_option(
        '--format', dest='format', default=None, type='string', metavar='FORMAT',
        help=' '.join([
            'set format to FORMAT in the summary command (default: "%s")' % DEFAULT_FORMAT,
            'The following symbols will be replaced.',
            '"%D" -> date,',
            '"%T" -> time,',
            '"%S" -> summary,',
            '"%C" -> creator,',
            '"%L" -> location',
        ])
    )
    p.add_option(
        '--separator', dest='separator', default=None, type='string', metavar='SEPARATOR',
        help='set date separator to SEPARATOR in the summary command (default: None)'
    )
    p.add_option(
        '--debug', dest='debug', action='store_true', default=False,
        help='enable debug logging (default: False)'
    )
    return p


parser = _get_parser()
