from __future__ import division, print_function, absolute_import, unicode_literals

from calendar_cli.operation.operation import Operation
from calendar_cli.setting.arg_parser import parser


class HelpOperation(Operation):
    def run(self):
        parser.print_help()
