#!/usr/bin/env python

import logging
from ltsense.transport import AbstractTransport
from os import path

class LocalFileTransport(AbstractTransport):

    def __init__(self, directory=None, file_extension='json'):
        self.directory = directory
        self.file_extension = file_extension
        self._sequence = 1
        AbstractTransport.__init__(self)

    def __next_file(self):
        while True:
            check = path.join(self.directory, '{}.{}'.format(self._sequence, self.file_extension))
            if not path.isfile(check):
                return check
            else:
                self._sequence += 1

    def send_package(self, payload):
        """Writes the payload to disk"""
        payload = AbstractTransport.send_package(self, payload)
        if self.directory is None:
            logging.error('No directory specified')
        elif not path.isdir(self.directory):
            logging.error('{} does not exist or is not a directory'.format(self.directory))
        else:
          next_file = path.join(self.__next_file())
          with open(next_file, 'w') as f:
              logging.debug("Writing data to {}".format(next_file))
              f.write(payload)
