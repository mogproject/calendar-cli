from __future__ import division, print_function, absolute_import, unicode_literals

import httplib2
import pytz
from apiclient import discovery
import oauth2client

from calendar_cli.operation.operation import Operation
from mog_commons.io import print_safe
from mog_commons.functional import omap, oget, ozip
from calendar_cli.i18n import *


class RegisterOperation(Operation):
    pass
