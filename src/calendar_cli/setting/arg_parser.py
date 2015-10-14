from __future__ import division, print_function, absolute_import, unicode_literals

import os
from optparse import OptionParser

VERSION = 'calendar-cli %s' % __import__('calendar_cli').__version__

USAGE = """
  %prog [options]
                        Print a summary of events on the calendar.

  %prog setup <secret_path> [--credential <credential_path>]
                        Generate a credentials file from the client secret.
                        You need a web browser to proceed.
"""


DEFAULT_CREDENTIAL_PATH = os.path.join(os.path.expanduser('~'), '.credentials', 'calendar-cli.json')


def _get_parser():
    p = OptionParser(usage=USAGE, version=VERSION)
    p.add_option(
        '--calendar', dest='calendar', default='primary', type='string', metavar='CALENDAR',
        help='set calendar id to CALENDAR (default:primary)'
    )
    p.add_option(
        '--date', dest='date', default=None, type='string', metavar='YYYYMMDD',
        help='set summary date to YYYYMMDD (default:today)'
    )
    p.add_option(
        '--credential', dest='credential', default=DEFAULT_CREDENTIAL_PATH, type='string', metavar='CREDENTIAL',
        help='set credential path to CREDENTIAL (default:%s)' % DEFAULT_CREDENTIAL_PATH
    )
    return p


parser = _get_parser()
