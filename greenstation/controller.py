#!/usr/bin/env python

from sensors import OneWireSensorHandler
from threading import Thread
import time

class AbstractController(Thread):
 
  def __init__(self):
    Thread.__init__(self)
    
    self.sampleRate = 10.0
    self.dataHandlers = None
    self.sensorHandlers = None
    self.transports = None
  
    self.sensorHandlers = []
    self.dataHandlers = []
    self.start()

  def run(self):
    while True:
      self.process_sensor_data()
      time.sleep(float(self.sampleRate))

  def process_sensor_data(self):
    if self.sensorHandlers != None:
      sensors = []
      for h in self.sensorHandlers:        
        sensors.extend( h.sensors )
      if self.dataHandlers != None:
        for d in self.dataHandlers:
          d.render_data(sensors)

class DefaultController(AbstractController):

  def __init__(self):
    AbstractController.__init__(self)
    
    #owpath = config.get('OneWire','owfsMount')
    #if owpath == None:
    #  raise Exception('Config','No OneWire/owfsMount defined')
       
    #self.sensorHandlers.append(OneWireSensorHandler(owpath))

