#!/usr/bin/env python

import os

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


class TemperatureSensor(AbstractSensor):

  def __init__(self,uid,dataFile):
    AbstractSensor.__init__(self)
    self.id = uid
    self.dataFile = dataFile

  def get_id(self):
    return self.id;
  
  def get_type(self):
    return "Temperature"

  def get_data(self):
    f = open(self.dataFile,'r')
    data = f.read()
    f.close()
    return data; 
    
  def get_units(self):
    pass    


class AbstractSensorHandler:

  def __init__(self):
    pass

  def get_sensors(self):
    pass


class OneWireSensorHandler(AbstractSensorHandler):

  def __init__(self,owfs_mount):
    AbstractSensorHandler.__init__(self)
    self.owfs_mount = owfs_mount  

  def get_sensors(self):
    path = os.listdir(self.owfs_mount)
    ret = []
    for p in path:
       (name,ext) = (os.path.splitext(p))
       try:
         stype = int( name )
         if(stype == 10):
           tfile = os.path.join(os.path.join(self.owfs_mount,p),'temperature')
           ret.append( TemperatureSensor(ext,tfile) )
       except ValueError:
         pass
    return ret

 
class GPSSensorHandler(AbstractSensorHandler):
  pass

    

class OneWireTempSensor(AbstractSensor):
  pass
  
class GPSSensor(AbstractSensor):
  pass
