#!/usr/bin/env python
from configobj import ConfigObj,Section
from validate import Validator
import logging


class BootStrap(object):

  config_specification = """
[General]

sample_rate = float

[Data]
  [[__many__]]
    type = option('sense.xml')
    transports = string
    sensors = list
      [Identification]
        type = option("name", "mac", "uuid")
        adapter = string
        name = string
        file = string

[Transport]
  [[__many__]]
    url = string
    pause_rate = float
    timeout = float
    type = option('http')
      [[[Queue]]]
        type = option('memory','sqlite')
        data = string
      [[Security]]
        type = option('none','rsa','m2')
        data_dir = string
        key_file = string
        key_size = integer

[Sensors]
  [[__many__]]
    type = option('virtual','1write/usb')
      [[[__many__]]]
        type = option('virtual/temp')
        id = string
        units = string
        rangeMin = integer
        rangeMax = integer
"""

#Taken from
# http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
  def _load_obj(self,name):
    components = name.split('.')
    path = '.'.join(components[:-1])
    clss = components[-1:][0]
    mod = __import__(path,globals(),locals(),clss)
    return getattr(mod,clss)()

  def _set_args(self,obj,key,value):
    logging.debug('Setting attribute %s to %s for class %s (type: %s)' % (key,value,obj,type(value)))
    setattr(obj,key,value)



  def proc(self,cfg,section=None,variable=None):
    for c in cfg:
      if c == 'General':
        logging.debug('Loading General Section')
      else:
        if type(cfg[c]) is Section:
          if c[0].isupper():
            if variable is None:
              logging.debug('Loading Section: {0} '.format(c))
              self.proc(cfg[c],c)
            else:
              pass
          else:
            tp = cfg[c]['type']
            logging.debug('Creating variable {0} with type {1}'.format(c,tp))
            logging.debug('ltsense.{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            self._object_map[c] = self._load_obj('{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            self.proc(cfg[c],section,c)
        else:
          logging.debug('Setting attribute {0} for {1}'.format(c,variable))
          #Anything starting with $ or is a list has delayed evaluation
          if (isinstance(cfg[c],basestring) and cfg[c][0] == '$') or isinstance(cfg[c],list):
            logging.debug("Delay evaluation for {0}".format(cfg[c]))
            self._delayed_eval[variable] = cfg[c]
          elif c == 'type':
            pass
          else:
            self._set_args(self._object_map[variable],c,cfg[c])
            #print('You want a ' + self.types[c][cfg[c]['type']])




  def __init__(self, filename):

    cfg = ConfigObj(filename, configspec=BootStrap.config_specification.split('\n'))
    test = cfg.validate(Validator(),copy=True)
    if not test:
      print("Invalid")

    self._section = {}
    self._vars = {}
    self._delayed_eval = {}
    self._object_map = {}

    self.namespaces = {'Identification' : 'identification' ,
                       'Queue' : 'queue'}

    self.types = { 'Identification' :
                  { 'name'  : 'NamedIdentifier' ,
                    'mac'  : 'MacAddressIdentifier' ,
                    'uuid' : 'UUIDIdentifier'} ,
              'Queue' :
                  { 'memory' : 'MemoryQueue' ,
                    'sqlite' : 'SQLiteQueue' },
              'Security' :
                  { 'rsa' : 'RSASecurity',
                    'm2'  : 'M2Security' },
              'Transport' :
                  { 'http' : 'http.QueuedHttpPostTransport' },
              'Data' :
                  { 'sense.xml' : 'SenseDataHandler' },
              'SensorHandlers' :
                  {  },
              'Sensors' :
                { 'virtual/temp' : 'virtual.RandomSensor',
                  'virtual/image' : 'virtual.ImageSensor',
                  'virtual' : 'handlers.GeneralSensorHandler',
                  '1wire/usb' : 'handlers.OWFSSensorHandler'}
            }


    self.proc(cfg)



