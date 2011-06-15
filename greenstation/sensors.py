#!/usr/bin/env python

import os
import logging
import fcntl, socket, struct

class AbstractSensor:

  def __init__(self):
     pass

  def get_id(self):
    return ('Unimplemented')
    
  def get_type(self):
    return ('Unimplemented')
    
  def get_data(self):
    return ('Unimplemented')
    
  def get_units(self):
    return ('Unimplemented')


class AbstractOWFSSensor(AbstractSensor):

  def __init__(self,uid,dataFile):
    AbstractSensor.__init__(self)
    self.id = uid
    self.dataFile = dataFile

  def get_id(self):
    return self.id;
  
  def get_data(self):
    f = open(self.dataFile,'r')
    data = f.read()
    f.close()
    return data; 
    

class TemperatureSensor(AbstractOWFSSensor):

  def get_type(self):
    return "Temperature"

  def get_units(self):
    return "C"

class CountingSensor(AbstractOWFSSensor):
  
  def get_type(self):
    return "Counter"

  def get_units(self):
    return "rev"

class AbstractSensorHandler:

  def __init__(self):
    pass

  def get_sensors(self):
    pass


class OneWireSensorHandler(AbstractSensorHandler):

  def __init__(self):
    AbstractSensorHandler.__init__(self)

  def set_owfs_mount(self,owfs_mount):
    self.owfs_mount = owfs_mount

  def get_sensors(self):
    path = os.listdir(self.owfs_mount)
    ret = []
    for p in path:
       (name,ext) = (os.path.splitext(p))
       if name == '10':
         tfile = os.path.join(os.path.join(self.owfs_mount,p),'temperature')
         ret.append( TemperatureSensor(ext.lstrip('.'),tfile) )
       if name == '1D':
         tfile =  os.path.join(os.path.join(self.owfs_mount,p),'counters.ALL')
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

  def get_id(self):
    return self.__getHwAddr()

  def get_type(self):
    return "Identifier"

  def get_data(self):
    return self.__getHwAddr()

  def get_units(self):
    return "Hex"

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
    self.__id = "Unimplemented"
    self.__type = "Unimplemented"
    self.__data = "Unimplemented"
    self.__units = "Unimplemented"

  def set_id(self,sid):
    self.__id = sid
  def set_type(self,stype):
    self.__type = stype
  def set_data(self,sdata):
    self.__data = sdata
  def set_units(self,units):
    self.__units = units

  def get_id(self):
    return self.__id
  def get_type(self):
    return self.__type
  def get_data(self):
    return self.__data
  def get_units(self):
    return self.__units
   
