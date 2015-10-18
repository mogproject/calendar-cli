from __future__ import division, print_function, absolute_import, unicode_literals

from calendar_cli.operation.operation import Operation
from calendar_cli.setting.arg_parser import parser
from mog_commons.io import print_safe


class HelpOperation(Operation):
    def __init__(self, exception=None):
        Operation.__init__(self, ('exception', exception))

    def run(self):
        parser.print_usage()
        if self.exception:
            print_safe('%s: %s' % (self.exception.__class__.__name__, self.exception))
