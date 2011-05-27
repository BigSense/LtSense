#!/usr/bin/env python

from sensors import OneWireSensorHandler
from threading import Thread
import time
import ConfigParser

class AbstractController(Thread):
  
  _sample_rate = 10
  
  def __init__(self,config):
    Thread.__init__(self)
    
    config_sample_rate = config.get('Global','SampleRate')
    if config_sample_rate != None:
      self._sample_rate = float(config_sample_rate)
    
    self.sensorHandlers = []
    self._dataHandler = None
    self.start()

  def run(self):
    while True:
      self.process_sensor_data()
      time.sleep(self._sample_rate)
  
  def set_data_handler(self,dataHandler):  
    self._dataHandler = dataHandler

  def process_sensor_data(self):
    if self.sensorHandlers != None:
      print(self.sensorHandlers)
      for h in self.sensorHandlers:        
        sensors = h.get_sensors()  
        print(sensors)
        print(self._dataHandler)
        if self._dataHandler != None and sensors != None:
          self._dataHandler.render_data(sensors)

class DefaultController(AbstractController):

  def __init__(self,config):
    AbstractController.__init__(self,config)
    
    owpath = config.get('OneWire','owfsMount')
    if owpath == None:
      raise Exception('Config','No OneWire/owfsMount defined')
       
    self.sensorHandlers.append(OneWireSensorHandler(owpath))

