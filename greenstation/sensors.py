#!/usr/bin/env python

import os
import logging
import fcntl, socket, struct


class AbstractSensor:

  def __init__(self):
     pass

  id = 'Unimplemented'
  type = 'Unimplemented'
  data = 'Unimplemented'
  units = 'Unimplemented'


class AbstractOWFSSensor(AbstractSensor):

  def __init__(self,uid,dataFile):
    AbstractSensor.__init__(self)
    self.id = uid
    self.dataFile = dataFile
  
  @property
  def data(self):
    f = open(self.dataFile,'r')
    data = f.read()
    f.close()
    return data; 
    

class TemperatureSensor(AbstractOWFSSensor):

  type = "Temperature"
  units = "C"

class CountingSensor(AbstractOWFSSensor):
  
  type = "Counter"
  units = "rev"

class AbstractSensorHandler:

  def __init__(self):
    pass

  def get_sensors(self):
    pass


class OneWireSensorHandler(AbstractSensorHandler):

  def __init__(self):
    AbstractSensorHandler.__init__(self)

  owfsMount = None  

  def get_sensors(self):
    path = os.listdir(self.owfsMount)
    ret = []
    for p in path:
       (name,ext) = (os.path.splitext(p))
       if name == '10':
         tfile = os.path.join(os.path.join(self.owfsMount,p),'temperature')
         ret.append( TemperatureSensor(ext.lstrip('.'),tfile) )
       if name == '1D':
         tfile =  os.path.join(os.path.join(self.owfsMount,p),'counters.ALL')
         ret.append( CountingSensor(ext.lstrip('.'),tfile) )
    
    return ret

 
class GeneralSensorHandler(AbstractSensorHandler):
  
  def __init__(self):
    AbstractSensorHandler.__init__(self)
    self.__sensors = []

  def set_sensors(self,sensors):
    self.__sensors = sensors

  def add_sensors(self,sensors):
    self.__sensors.extend(sensors)
  
  def get_sensors(self):
    return self.__sensors


class MacAddressIdentificationSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.__adapter = 'eth0'

  @property 
  def id(self):
    return self.__getHwAddr()

  type = "Identifier"

  @property 
  def data():
    return self.__getHwAddr()

  units = "Hex"

  def set_adapter(self,adapter):
    self.__adapter = adapter

  #Taken from http://stackoverflow.com/questions/159137/getting-mac-address
  def __getHwAddr(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', self.__adapter[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]



class StaticInformationSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.id = "Unimplemented"
    self.type = "Unimplemented"
    self.data = "Unimplemented"
    self.units = "Unimplemented"

   
