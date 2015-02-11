#!/usr/bin/env python

import fcntl
import socket
import struct
import uuid
from os import path


class AbstractIdentifier(object):

    def __init__(self):
        object.__init__(self)

    def identify(self):
        return 'Unimplemented'


class MacAddressIdentifier(AbstractIdentifier):

    def __init__(self):
        AbstractIdentifier.__init__(self)
        self.adapter = 'eth0'

    def identify(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', self.adapter[:15]))
        return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


class NamedIdentifier(AbstractIdentifier):

    def __init__(self):
        AbstractIdentifier.__init__(self)
        self.id = 'Unknown'

    def identify(self):
        return self.id


class UUIDIdentifier(AbstractIdentifier):

    id_file = property(lambda self: self._id_file, lambda self, value: self._init_id_file(value))

    def __init__(self):
        AbstractIdentifier.__init__(self)
        self.id_file = 'uuid'

    def _init_id_file(self, value):
        if path.isfile(value):
            with open(value, 'r') as ufile:
                self.__id = ufile.read()
        else:
            self.__id = str(uuid.uuid4())
            with open(value, 'w') as ufile:
                ufile.write(self.__id)

    def identify(self):
        return self.__id
