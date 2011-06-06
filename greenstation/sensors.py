#!/usr/bin/env python

import os
import logging

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

 
class GPSSensorHandler(AbstractSensorHandler):
  pass

  
class GPSSensor(AbstractSensor):
  pass
