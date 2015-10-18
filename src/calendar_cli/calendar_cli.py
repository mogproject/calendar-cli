from __future__ import division, print_function, absolute_import, unicode_literals

import sys

from calendar_cli.setting.setting import Setting
from mog_commons.io import print_safe


def main():
    """
    Main function
    """

    setting = None
    try:
        setting = Setting().parse_args(sys.argv)
        return_code = setting.operation.run()
    except KeyboardInterrupt:
        return_code = 3
    except Exception as e:
        if setting is None or setting.debug:
            import traceback
            traceback.print_exc()
        else:
            print_safe('%s: %s' % (e.__class__.__name__, e))
        return_code = 2
    return return_code
