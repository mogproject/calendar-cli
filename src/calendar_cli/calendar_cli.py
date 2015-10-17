from __future__ import division, print_function, absolute_import, unicode_literals

import sys
from calendar_cli.setting.setting import Setting
from mog_commons.io import print_safe


def main():
    """
    Main function
    """

    try:
        return_code = Setting().parse_args(sys.argv).operation.run()
    except KeyboardInterrupt:
        return_code = 3
    except Exception as e:
        print_safe('%s: %s' % (e.__class__.__name__, e))
        # import traceback
        # print(traceback.print_exc())
        return_code = 2
    return return_code
