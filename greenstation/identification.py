#!/usr/bin/env python

import fcntl, socket, struct 

class AbstractIdentifier(object):
  
  def AbstractIdentifier(self):
    object.__init__(self)
    
  def idenfity():
    return 'Unimplemented'
    
class MacAddressIdentifier(AbtractIdentifier):
  
  def MacAddressIdentifier(self):
    AbstractIdentifier.__init__(self)
    self.adapter = 'eth0'
    
  def identify():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', self.adapter[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    
class UUIDIdentifier(AbstractIdentifier):
  
  def UUIDIdentifier(self):
    AbstractIdentifier.__init__(self)