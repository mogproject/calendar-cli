from __future__ import division, print_function, absolute_import, unicode_literals

import sys
from calendar_cli.setting.setting import Setting


def main():
    """
    Main function
    """

    try:
        return_code = Setting().parse_args(sys.argv).operation.run()
    except Exception as e:
        print('%s: %s' % (e.__class__.__name__, e))
        # import traceback
        # print(traceback.print_exc())
        return_code = 2
    return return_code
