#!/usr/bin/env python

from sensors import OneWireSensorHandler

class AbstractController:
  
  sample_rate = 100
  
  
class DefaultController(AbstractController):

  def __init__(self):
    hOwfs = OneWireSensorHandler('/var/lib/owfs/mnt')
    AbstractSensorHandler h = hOwfs.get_sensors()
    
