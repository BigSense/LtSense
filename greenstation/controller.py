#!/usr/bin/env python

from sensors import OneWireSensorHandler
from threading import Thread
import time

class AbstractController(Thread):
  
  _sample_rate = 10
  
  def __init__(self):
    Thread.__init__(self)
    
    self.sensorHandlers = []
    self._dataHandler = None
    self.start()

  def set_sample_rate(self,rate):
    self._sample_rate = float(rate)

  def run(self):
    while True:
      self.process_sensor_data()
      time.sleep(self._sample_rate)
  
  def set_data_handler(self,dataHandler):  
    self._dataHandler = dataHandler

  def set_sensor_handlers(self,sensorHandlers):
    self.sensorHandlers = sensorHandlers

  def process_sensor_data(self):
    if self.sensorHandlers != None:
      for h in self.sensorHandlers:        
        sensors = h.get_sensors()  
        if self._dataHandler != None and sensors != None:
          self._dataHandler.render_data(sensors)

class DefaultController(AbstractController):

  def __init__(self):
    AbstractController.__init__(self)
    
    #owpath = config.get('OneWire','owfsMount')
    #if owpath == None:
    #  raise Exception('Config','No OneWire/owfsMount defined')
       
    #self.sensorHandlers.append(OneWireSensorHandler(owpath))

