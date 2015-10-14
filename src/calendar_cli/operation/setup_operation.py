from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import os
import argparse
import oauth2client
from calendar_cli.operation.operation import Operation
from calendar_cli.util import universal_print


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


class SetupOperation(Operation):
    """
    Create the credentials file from a client secret file.
    """

    def __init__(self, secret_path, credential_path):
        Operation.__init__(self, ('secret_path', secret_path), ('credential_path', credential_path))

    def run(self):
        assert not os.path.exists(self.credential_path), 'Credential file already exists: %s' % self.credential_path

        flow = oauth2client.client.flow_from_clientsecrets(self.secret_path, SCOPES)
        store = oauth2client.file.Storage(self.credential_path)
        flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args('')

        parent_dir = os.path.dirname(self.credential_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        credentials = oauth2client.tools.run_flow(flow, store, flags)
        assert credentials is not None and not credentials.invalid, 'Failed to create credential file.'

        universal_print(sys.stdout, 'Saved credential file: %s\n' % self.credential_path)
        return 0
