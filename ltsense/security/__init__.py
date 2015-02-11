#!/usr/bin/env python
__author__ = 'Sumit Khanna <sumit@penguindreams.org>'


class DataSecurity(object):

    def __init__(self):
        object.__init__(self)
        self.data_dir = None
        self.ready = False
        self.key_file = 'key.pem'
        self.key_size = 2048
        self._key = None

    def initalize_security(self):
        pass

    def sign_data(self, data):
        return 'Unimplemented'
