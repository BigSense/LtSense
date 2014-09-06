import os
import logging
import time

from ltsense.sensors import AbstractOneWireSensor



## --- Command Line Based One Wire Sensors --- ###
##  Not sure if I want to get rid of this yet. Should we keep around support for counting sensors?
"""
class TemperatureSensor(AbstractOneWireSensor):

  def __init__(self,unique_id,extProc):
    AbstractOneWireSensor.__init__(self,unique_id,extProc)
    self.type = "Temperature"
    self.units = "C"

class CountingSensor(AbstractOneWireSensor):
  
  def _read_count(self):
    return float(self._read_data().split(':')[2])

class FluidVolumeSensor(CountingSensor):
  
  def __init__(self):
    AbstractOneWireSensor.__init__(self,None,None)
    self.type = "Volume"
    self.units = "Undefined"
    self.bucket_volume = float(0)
    self.__initial_count = -1
    self.countDir = None

  def _read_bucket_data(self):
    
    self.current = self._read_count()
    
    if self.__initial_count == -1:
      
      if self.countDir != None and os.path.isdir(self.countDir):
        
        countFile = os.path.join(self.countDir,self.id)
        
        if(os.path.isfile(countFile)):
          fd = open(countFile)
          self.__initial_count = float(fd.readlines()[0].strip())
          fd.close()
          logging.debug('Read existing initial count file %s with count %s' % (countFile,self.__initial_count))
        else:
          fd = open(countFile,'w')
          fd.write(str(self.current))
          self.__initial_count = self.current
          fd.close()
          logging.debug('Created initial count file %s with count %s' % (countFile,self.__initial_count))
      else:
        self.__initial_count = self.current
        logging.debug('Counter Initially Set to %s (Volume: %s %s). No History set' % (self.__initial_count, (float(self.__initial_count) * float(self.bucket_volume)), self.units))        
    

    logging.debug('Initial Count %s' % self.__initial_count)
    logging.debug('Current %s' % self.current)
    offset = self.current - float(self.__initial_count)
    return str(  float(offset) * float(self.bucket_volume) )

  data = property(_read_bucket_data,lambda self,v:None )
  
class HistoryCountingSensor(CountingSensor):
  
  def __init__(self):
    AbstractOneWireSensor.__init__(self,None,None)
    self.type = "HistoryCounting"
    self._units = "Undefined"
    self._time_stamp = float(0)
    self._count = None

  def _read_delta(self):

      #first time, initalize to zero
      if self._count == None:
        self._count = float(self._read_count())
        self._time_stamp = float(time.time())
        return (self._time_stamp,0)

      #Time duration 
      now = float(time.time())
      ptime = float(now - self._time_stamp)
      self._time_stamp = now

      cur = float(self._read_count()) 
      delta = cur - float(self._count) 
      self._count = cur
      
      return (ptime,delta)   
  
    
class FlowRateSensor(HistoryCountingSensor):
  
  def __init__(self):
    HistoryCountingSensor.__init__(self)
    self.type = "FlowRate"
    self._units = "Undefined"
    self.bucket_volume = float(0)
  
  def _read_bucket_data(self):
    
    (ptime,delta) = self._read_delta()
    vol = delta * float(self.bucket_volume)
    
    # returns units per second
    return str( (vol / ptime) ) 
  
  data = property(_read_bucket_data,lambda self,v:None )
  
  units = property(lambda self: ('%s/s' % self._units) , lambda self,v: setattr(self,'_units',v) )  

class WindSpeedSensor(HistoryCountingSensor):
  
  def __init__(self,sensor_id,process):
    HistoryCountingSensor.__init__(self)
    self.extProc = process
    self.id = sensor_id
    self.type = "WindSpeed"
    self.units = "kph"
      
  def _read_bucket_data(self):
    
    (ptime,delta) = self._read_delta()
    
    #Taken from 1-Wire manual: count / time / 2 * 2.453 (constant/co-efficent)
    mph = delta / ptime / 2 * 2.453
    kph = mph * 1.609344
    return str(kph)
    
  data = property(_read_bucket_data,lambda self,v:None )    """