#!/usr/bin/env python

from threading import Thread
import time
import ltsense
import logging
import sys

class AbstractController(Thread):
 
  def __init__(self):
    Thread.__init__(self)
    
    self.sampleRate = 10.0
    self.dataHandlers = None
    self.sensorHandlers = None
    self.transports = None
  
    self.sensorHandlers = []
    self.dataHandlers = []

  def run(self):
    while not ltsense.exit_all_threads:
      self.process_sensor_data()
      time.sleep(float(self.sampleRate))
    logging.info('Exit Detected. Stopping Controller Thread')

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
    self.start()
    
class RespawningController(AbstractController):

  def __init__(self):
    AbstractController.__init__(self)
    #default, exit if we respawn more than 10
    # times in 10 seconds
    self.respawnRateLimit = 10
    self.respawnTimeLimit = 10
    self.start()
 
  def run(self):
    spawnCount = 0
    spawnTime = int(time.time())

    
    
    try:
      AbstractController.run()
    except:
      logging.error('Main Process Loop Generated an Exception: %s' % sys.exc_info()[0])
   
