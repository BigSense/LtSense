#!/usr/bin/env python

import os
import logging
import fcntl, socket, struct
import time


class AbstractSensor(object):

  def __init__(self):
    object.__init__(self)
    self.id = 'Unimplemented'
    self.type = 'Unimplemented'
    self.data = 'Unimplemented'
    self.units = 'Unimplemented'


class AbstractOWFSSensor(AbstractSensor):


  def __init__(self,uid,dataFile):
    AbstractSensor.__init__(self)
    self.id = uid
    self.dataFile = dataFile
  
  def _read_data(self):
    f = open(self.dataFile,'r')
    data = f.read()
    f.close()
    return data
    
  data = property(_read_data,lambda self,v:None )

class TemperatureSensor(AbstractOWFSSensor):

  def __init__(self,uid,dataFile):
    AbstractOWFSSensor.__init__(self,uid,dataFile)
    self.type = "Temperature"
    self.units = "C"

class CountingSensor(AbstractOWFSSensor):
  
  def __init__(self,uid,dataFile):
    AbstractOWFSSensor.__init__(self,uid,dataFile)
    self.type = "Counter"
    self.units = "rev"
    
class RainBucketSensor(AbstractOWFSSensor):
  
  def __init__(self,):
    AbstractOWFSSensor.__init(self,None,None)
    self.type = "FlowRate"
    self.units = "Undefined"
    self.bucket_volume = float(0)
    self._time_stamp = float(0)
    
  data = property(_read_bucket_data,lambda self,v:None )
  
  def _read_bucket_data(self):
    #Time duration 
    now = float(time.time())
    ptime = float(now - self._time_stamp)
    self._time_stamp = now
    
    vol = float(AbstractOWFSSensor.data) * float(self.bucket_volume)
    
    # returns units per second
    return vol / ptime 
    
        
    
  

class AbstractSensorHandler(object):

  def __init__(self):
    object.__init__(self)
    self.sensors = []


class OneWireSensorHandler(AbstractSensorHandler):

  def __init__(self):
    AbstractSensorHandler.__init__(self)
    self.owfsMount = None  
  
  def _get_sensors(self):
    path = os.listdir(self.owfsMount)
    ret = []
    for p in path:
       (name,ext) = (os.path.splitext(p))
       if name == '10':
         tfile = os.path.join(os.path.join(self.owfsMount,p),'temperature')
         ret.append( TemperatureSensor(ext.lstrip('.'),tfile) )
       if name == '1D':
         tfile =  os.path.join(os.path.join(self.owfsMount,p),'counters.ALL')
         bucket = greenstation.loader.get_class('RainBucketSensor')
         bucket.dataFile = tfile
         bucket.id = ext.lstrip('.')
         ret.append(bucket)         
         #ret.append( CountingSensor(ext.lstrip('.'),tfile) )
    
    return ret

  sensors = property(_get_sensors,lambda self,v:None )
 
class GeneralSensorHandler(AbstractSensorHandler):
  
  def __init__(self):
    AbstractSensorHandler.__init__(self)

  def add_sensors(self,sensors):
    self.sensors.append(sensors)

"""
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
"""


class StaticInformationSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.id = "Unimplemented"
    self.type = "Unimplemented"
    self.data = "Unimplemented"
    self.units = "Unimplemented"

   
