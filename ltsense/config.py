#!/usr/bin/env python
from configobj import ConfigObj,Section
from validate import Validator
import logging
from ltsense.controller import DefaultController


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



  def __process(self,cfg,section=None,variable=None):
    """Recursively processes a configuration object"""
    for c in cfg:
      if c == 'General':
        logging.debug('Loading General Section')
        self._controller.sample_rate = cfg[c]['sample_rate']
      else:
        if type(cfg[c]) is Section:
          if c[0].isupper():
            if variable is None:
              logging.debug('Loading Section: {0} '.format(c))
              self.__process(cfg[c],c)
            else:
              #Anonymous Sections are a little special
              # we don't reuse them so they don't get their own sections
              # We're going to create delayed eval variables and give them the name
              # basevar$section
              cfg[c] = "{0}${1}".format(variable,c)
              self._delayed_eval[cfg[c]] = (variable,c.lower())
          else:
            if variable is not None:
              # this is for one case, and that's Sensors
              if variable not in self._delayed_eval:
                self._delayed_eval[variable] = ('sensors',"${0}".format([cfg[c]]))
              # ARGG Fuck all this shit!
              #if self._delayed_eval[variable]
              #self.__process(cfg[c],c)
            else:
              tp = cfg[c]['type']
              logging.debug('Creating variable {0} with type {1}'.format(c,tp))
              logging.debug('ltsense.{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
              self._object_map[c] = self._load_obj('{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
              if section == 'Data':
                self._data_handlers.append(self._object_map[c])
              if section == 'Sensors' and self.types[section][cfg[c]['type']].split('.')[0] == 'handlers':
                self._sensor_handlers.append(self._object_map[c])
              self.__process(cfg[c],section,c)
        else:
          #Anything starting with $ or is a list has delayed evaluation
          if (isinstance(cfg[c],basestring) and cfg[c][0] == '$') or isinstance(cfg[c],list):
            logging.debug("Delay evaluation for {0}".format(cfg[c]))
            self._delayed_eval[variable] = (c,cfg[c])
          elif c == 'type':
            pass
          else:
            logging.debug('Setting attribute {0} for {1}'.format(c,variable))
            self._set_args(self._object_map[variable],c,cfg[c])
            #print('You want a ' + self.types[c][cfg[c]['type']])

  def __eval_item(self,item):
    """Used for deferred evaluation variables (those that start with $) and lists.
      Items in list starting with $ will be substituted for defined objects.
      All other list items will be treated as string.
    """
    if isinstance(item,list):
      #Substitute all variables (start with $)
      for i,j in enumerate(item):
        if j[0] == '$':
          item[i] = self._object_map(j[1:])
      return item
    else:
      return item[1:]


  def __init__(self, filename):

    self._delayed_eval = {}
    self._object_map = {}
    self._controller = DefaultController()

    self._data_handlers = []
    self._sensor_handlers = []

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
              'Sensors' :
                { 'virtual/temp' : 'virtual.RandomSensor',
                  'virtual/image' : 'virtual.ImageSensor',
                  'virtual' : 'handlers.GeneralSensorHandler',
                  '1wire/usb' : 'handlers.OWFSSensorHandler'}
            }

    cfg = ConfigObj(filename, configspec=BootStrap.config_specification.split('\n'))
    test = cfg.validate(Validator(),copy=True)
    if not test:
      print("Invalid")

    self.__process(cfg)
    for var,(attr,val) in self._delayed_eval.items():
      item = self.__eval_item(val)
      logging.debug("Setting object {0}, {1} = {2}".format(var,attr,item))
      self._set_args(self._object_map[var], attr, self._object_map( item ))

    self._controller.data_handlers = self._data_handlers
    self._controller.sensor_handlers = self._sensor_handlers





