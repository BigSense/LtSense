# --- Sensor Handlers --- #
from ltsense.sensors import AbstractSensorHandler
from ltsense.sensors.owproc import TemperatureSensor,WindSpeedSensor
import logging
from ltsense import loader

class AgraNetSensorHandler(AbstractSensorHandler):
    
  def __init__(self):
    AbstractSensorHandler.__init__(self)
    self.extProcess = None
    self.__sensor_cache = {}
    self.counterType = 'Fluid'

  def __load_multi_cached_sensor(self,id,process,objname):
    if id not in self.__sensor_cache:
      sbuild = loader.get_class(objname,True)
      sbuild.extProc = process
      sbuild.id = id
      self.__sensor_cache[id] = sbuild
    return self.__sensor_cache[id]

  def __get_sensors(self):
    if self.extProcess == None:
      logging.warning('No subprocess given for AgraNetSensorHandler')
      return []
    else:
      ret = []
      self.extProcess.write_line('list')
      num_sensors = int(self.extProcess.read_line())
      for i in range(num_sensors):
        sensor_id = self.extProcess.read_line().strip()
        family = sensor_id[-2:].strip()
        if family == '10':
          if sensor_id not in self.__sensor_cache: 
            self.__sensor_cache[sensor_id] = TemperatureSensor(sensor_id,self.extProcess)
          ret.append( self.__sensor_cache[sensor_id] )
        if family == '1D':
          if self.counterType == 'Fluid':
            ret.append(self.__load_multi_cached_sensor(sensor_id + '-V',self.extProcess,'FluidVolumeSensor'))
            ret.append(self.__load_multi_cached_sensor(sensor_id + '-FR',self.extProcess,'FlowRateSensor'))          
          elif self.counterType == 'AirSpeed':
            if sensor_id not in self.__sensor_cache:
              self.__sensor_cache[sensor_id] = WindSpeedSensor(sensor_id,self.extProcess)
            ret.append( self.__sensor_cache[sensor_id] )
      
      return ret  
       

  sensors = property(__get_sensors,lambda self,v:None)  

  
class GeneralSensorHandler(AbstractSensorHandler):
  
  def __init__(self):
    AbstractSensorHandler.__init__(self)

  def add_sensors(self,sensors):
    self.sensors.append(sensors)
