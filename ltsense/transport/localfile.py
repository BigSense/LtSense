#!/usr/bin/env python

import logging
from ltsense.transport import AbstractTransport
from os import path

class LocalFileTransport(AbstractTransport):

    def __init__(self, directory=None, file_extension='json'):
        self.directory = directory
        self.file_extension = file_extension
        AbstractTransport.__init__(self)

    def send_package(self, payload):
        """Writes the payload to disk"""
        payload = AbstractTransport.send_package(self, payload)
        if directory is None:
            logging.error('No directory ')
        with open(path.join())
