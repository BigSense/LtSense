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
    print("Value " + str(value))
    print("Type " + str(type(value)))
    logging.debug('Setting attribute %s to %s for class %s' % (key,value,obj))
    setattr(obj,key,value)



  def proc(self,cfg,section=None,variable=None):
    for c in cfg:
      if c == 'General':
        print('General Sec')
      else:
        if type(cfg[c]) is Section:
          if c[0].isupper():
            if variable is None:
              print('You are in a section: '+c)
              self.proc(cfg[c],c)
            else:
              print('You are in section for a variable')
          else:
            tp = cfg[c]['type']
            print('You want a named variable: '+ c + ' (with type ' + tp + ')')
            print('ltsense.{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            self._object_map[c] = self._load_obj('{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            self.proc(cfg[c],section,c)
        else:
          print("You want a attribute: " + c + " for " + variable )
          #Anything starting with $ or is a list has delayed evaluation
          if (isinstance(cfg[c],basestring) and cfg[c][0] == '$') or isinstance(cfg[c],list):
            print("Delay eval for" +  str(cfg[c]))
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
                  { 'virtual' : 'handlers.GeneralSensorHandler' ,
                    '1wire/usb' : 'handlers.OWFSSensorHandler' },
              'Sensors' :
                { 'virtual/temp' : 'sensors.virtual.RandomSensor',
                  'virtual/image' : 'sensors.virtual.ImageSensor'}
            }


    self.proc(cfg)



