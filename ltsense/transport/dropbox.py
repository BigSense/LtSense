#!/usr/bin/env python


import logging
from ltsense.transport import QueuedTransport

# Include the Dropbox SDK libraries
from dropbox import client, rest, session


class QueuedDropboxTransport(QueuedTransport):

    def __init__(self):
        self.url = None
        QueuedTransport.__init__(self)
        self.appKey = None
        self.appSecret = None
        self.accessType = None
        self.__session = None

    def _run_transport(self, payload):
        # cache the session?
        if self.__session == None:
            self.__session = session.DropboxSession(self.appKey, self.appSecret, self.accessType)

        # Do some transport code here
