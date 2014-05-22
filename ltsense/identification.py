#!/usr/bin/env python

import fcntl, socket, struct 
import uuid
from os import path

class AbstractIdentifier(object):
  
  def __init__(self):
    object.__init__(self)
    
  def identify():
    return 'Unimplemented'
    
class MacAddressIdentifier(AbstractIdentifier):
  
  def __init__(self,adapter = 'eth0'):
    AbstractIdentifier.__init__(self)
    self.adapter = adapter
    
  def identify(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', self.adapter[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

class NamedIdentifier(AbstractIdentifier):
  
  def __init__(self,id='Unknown'):
    AbstractIdentifier.__init__(self)
    self.id = id
  
  def identify(self):
    return self.id
    
class UUIDIdentifier(AbstractIdentifier):
  
  id_file = property(lambda self : self._id_file,lambda self,value:self._init_id_file(value) )
  
  def __init__(self, id_file='uuid'):
    AbstractIdentifier.__init__(self)
    self.__id = ''
    self.id_file = id_file
    
  def _init_id_file(self,value):
    if path.isfile(value):
      with open(value,'r') as ufile:
        self.__id = ufile.read()
    else:  
      self.__id = str(uuid.uuid4())
      with open(value,'w')  as ufile:
        ufile.write(self.__id)
    
  def identify(self):
    return self.__id 
        
    
    
  