#!/usr/bin/env python

import os
import logging
import fcntl, socket, struct
import time
import loader


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

class FluidVolumeSensor(AbstractOWFSSensor):
  
  def __init__(self):
    AbstractOWFSSensor.__init__(self,None,None)
    self.type = "Volume"
    self.units = "Undefined"
    self.bucket_volume = float(0)
    self.reset_on_startup = False
    self.__initial_count = -1

  def _read_bucket_data(self):
    
    if self.__initial_count == -1:
      if self.reset_on_startup == True:
        self.__initial_count = self._read_data()
        logging.debug('Counter Initially Set to %s (Volume: %s %s)' % (self.__initial_count, (float(self.__initial_count) * float(self.bucket_volume)), self.units))
        return str(0.0)
      else:
        logging.debug('Counter Reset Set to False')
        self.__initial_count = 0
    
    cur = int(self._read_data()) - int(self.__initial_count)
    return str(  float(cur) * float(self.bucket_volume) )

  data = property(_read_bucket_data,lambda self,v:None )
  
    
class FlowRateSensor(AbstractOWFSSensor):
  
  def __init__(self):
    AbstractOWFSSensor.__init__(self,None,None)
    self.type = "FlowRate"
    self._units = "Undefined"
    self.bucket_volume = float(0)
    self._time_stamp = float(0)
    self._count = None
  
  def _read_bucket_data(self):
    
    #first time, initalize to zero
    if self._count == None:
      self._count = float(self._read_data())
      self._time_stamp = time.time()
      return str(0)
    
    #Time duration 
    now = float(time.time())
    ptime = float(now - self._time_stamp)
    self._time_stamp = now
    
    cur = float(self._read_data()) 
    delta = cur - float(self._count)
    self._count = cur 
    
    vol = delta * float(self.bucket_volume)
    
    # returns units per second
    return str( (vol / ptime) ) 
  
  data = property(_read_bucket_data,lambda self,v:None )
  
  units = property(lambda self: ('%s/s' % self._units) , lambda self,v: setattr(self,'_units',v) )  
  

class AbstractSensorHandler(object):

  def __init__(self):
    object.__init__(self)
    self.sensors = {} 


class OneWireSensorHandler(AbstractSensorHandler):

  def __init__(self):
    AbstractSensorHandler.__init__(self)
    self.owfsMount = None 
    self.counters = {} 
    self.__sensor_cache = {} 

  def __load_multi_cached_sensor(self,id,file,objname):
    if id not in self.__sensor_cache:
      sbuild = loader.get_class(objname,True)
      sbuild.dataFile = file
      sbuild.id = id
      self.__sensor_cache[id] = sbuild
    return self.__sensor_cache[id]    
 
  def __get_sensors(self):
    path = os.listdir(self.owfsMount)
    ret = []
    for p in path:
       (name,ext) = (os.path.splitext(p))
       sensor_id = ext.lstrip('.')
       if name == '10':
         if sensor_id not in self.__sensor_cache: 
           tfile = os.path.join(os.path.join(self.owfsMount,p),'temperature')
           self.__sensor_cache[sensor_id] = TemperatureSensor(sensor_id,tfile)
         ret.append( self.__sensor_cache[sensor_id] )
       if name == '1D':

         tfile =  os.path.join(os.path.join(self.owfsMount,p),'counters.A')
         
         ret.append(self.__load_multi_cached_sensor(sensor_id + '-V',tfile,'FluidVolumeSensor'))
         ret.append(self.__load_multi_cached_sensor(sensor_id + '-FR',tfile,'FlowRateSensor'))
    
    return ret

  sensors = property(__get_sensors,lambda self,v:None )
 
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

   
