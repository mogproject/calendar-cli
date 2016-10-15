from __future__ import division, print_function, absolute_import, unicode_literals

import os
import argparse
import oauth2client.tools
from calendar_cli.operation.operation import Operation
from mog_commons.io import print_safe


SCOPE_READ_WRITE = 'https://www.googleapis.com/auth/calendar'
SCOPE_READ_ONLY = 'https://www.googleapis.com/auth/calendar.readonly'


class SetupOperation(Operation):
    """
    Create the credentials file from a client secret file.
    """

    def __init__(self, secret_path, credential_path, read_only, no_browser):
        Operation.__init__(self,
                           ('secret_path', secret_path),
                           ('credential_path', credential_path),
                           ('read_only', read_only),
                           ('no_browser', no_browser))

    def run(self):
        assert not os.path.exists(self.credential_path), 'Credential file already exists: %s' % self.credential_path

        scopes = [SCOPE_READ_ONLY if self.read_only else SCOPE_READ_WRITE]
        flow = oauth2client.client.flow_from_clientsecrets(self.secret_path, scopes)
        store = oauth2client.file.Storage(self.credential_path)
        args = ['--noauth_local_webserver'] if self.no_browser else []
        flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args)

        parent_dir = os.path.dirname(self.credential_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        credentials = oauth2client.tools.run_flow(flow, store, flags)
        assert credentials is not None and not credentials.invalid, 'Failed to create credential file.'

        print_safe('Saved credential file: %s' % self.credential_path)
        return 0
