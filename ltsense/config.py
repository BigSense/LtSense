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
      [[[Identification]]]
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
      [[[Security]]]
        type = option('none','rsa','m2')
        data_dir = string
        key_file = string
        key_size = integer

[Handlers]
  [[__many__]]
    type = option('virtual/temp')
    sensors = string

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
    logging.debug('Setting attribute {0} to {1} for class {2} (type: {3})'.format(key,value,obj,type(value)))
    setattr(obj,key,value)


  def __add_delay_eval(self,var,attr,val):
    if var not in self._delayed_eval:
      self._delayed_eval[var] = {}
    self._delayed_eval[var][attr] = val

  def __create_variable(self,cfg,section,var):
    tp = cfg['type']
    logging.debug('Creating variable {0} with type {1}'.format(var,tp))
    if tp == 'none':
      self._object_map[var] = None
    else:
      logging.debug('\t>>ltsense.{0}.{1}'.format(section.lower(),self.types[section][tp]))
      self._object_map[var] = self._load_obj('{0}.{1}'.format(section.lower(),self.types[section][tp]))

  def __process(self,cfg,section=None,variable=None):
    """Recursively processes a configuration object"""
    for c in cfg:
      if type(cfg[c]) is Section:
        if c == 'General':
          logging.debug('Loading General Section')
          logging.debug('Sample Rate: {0}'.format(cfg[c]['sample_rate']))
          self._controller.sample_rate = cfg[c]['sample_rate']
        elif c[0].isupper() and section is None:
          logging.debug('Loading Section: {0} '.format(c))
          self.__process(cfg[c],c)
        elif c[0].isupper() and section is not None:
          av = "$${0}.{1}".format(section.lower(),c)
          logging.debug('Loading Anonymous Variable {0} with Type: {1}'.format(av,c))
          self.__create_variable(cfg[c],c,av)
          self.__add_delay_eval(variable,section.lower(),av)
          self.__process(cfg[c],c,av)
        else:
          var = "${0}".format(c)
          logging.debug('Loading Variable: {0}'.format(var))
          self.__create_variable(cfg[c],section,var)
          self.__process(cfg[c],section,var)
      else:
        #Anything starting with $ or is a list has delayed evaluation
        if (isinstance(cfg[c],basestring) and cfg[c][0] == '$') or isinstance(cfg[c],list):
          logging.debug("Delay evaluation for {0}".format(cfg[c]))
          self.__add_delay_eval(variable,c,cfg[c])
        elif c == 'type':
          pass
        else:
          self._set_args(self._object_map[variable],c,cfg[c])


  def __eval_item(self,item):
    """Used vy __eval_delays for deferred evaluation variables (those that start with $) and lists.
      Items in list starting with $ will be substituted for defined objects.
      Non-list items don.
    """
    if isinstance(item,list):
      #Substitute all variables (start with $)
      for i,j in enumerate(item):
        if j[0] == '$':
          item[i] = self._object_map[j[1:]]
      return item
    else:
      return self._object_map[item]

  def __eval_delays(self):
    """Call after a successful __process to assign all delayed variables"""
    for var in self._delayed_eval:
      for i,j in self._delayed_eval[var].items():
        item = self.__eval_item(j)
        logging.debug("Setting object {0}, {1} = {2}".format(var,i,item))
        self._set_args(self._object_map[var], i, item )

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
                  'virtual/image' : 'virtual.ImageSensor' },
              'Handlers' :
                { 'virtual' : 'GeneralSensorHandler',
                  '1wire/usb' : 'OWFSSensorHandler'},
            }

    cfg = ConfigObj(filename, configspec=BootStrap.config_specification.split('\n'))
    test = cfg.validate(Validator(),copy=True)
    if not test:
      #TODO: expand this
      print("Invalid")
      exit(3)

    self.__process(cfg)
    self.__eval_delays()

    self._controller.data_handlers = self._data_handlers
    self._controller.sensor_handlers = self._sensor_handlers





