#!/usr/bin/env python
from configobj import ConfigObj,Section
import logging
import ast
from ltsense.data import SenseDataHandler
from ltsense.identification import MacAddressIdentifier,UUIDIdentifier,NamedIdentifier
from ltsense.queue import MemoryQueue, SQLiteQueue
from ltsense.security.m2crypto import M2Security
from ltsense.security.pypiRsa import RSASecurity
from ltsense.transport.http import QueuedHttpPostTransport


class BootStrap(object):


  """def _identity(self,idsec):
    if idsec['type'] == "name":
      return NamedIdentifier(idsec['name'])
      return n
    elif idsec['type'] == "mac":
      return MacAddressIdentifier(idsec['adapter'])
    elif idsec['type'] == "uuid":
      return UUIDIdentifier(idsec['file'])
    else:
      return None

  def _queue(self,qsec):
      if qsec['type'] == 'memory':
        return MemoryQueue()
      elif qsec['type'] == 'sqlite':
        q = SQLiteQueue()
        q.data_file = qsec['data']
        return q
      else:
        return None

  def _security(self,ssec):
    s = None
    if ssec['type'] == "rsa":
      s = RSASecurity()
    elif ssec['type'] == "m2":
      s = M2Security()
    elif ssec['type'] == "none":
      s = None

    if s is None:
      return None
    else:
      s.data_dir = ssec['data_dir']
      s.key_file = ssec['key_file']
      s.key_size = ssec['key_size']
      return s

  def __transports(self):
    tsec = self.__cfg['Transports']
    trans = {}
    for t in tsec:
      tran = QueuedHttpPostTransport()
      tran.url = tsec[t]['url']
      tran.format = tsec[t]['format']
      tran.pause_rate = tsec[t]['pause_rate']
      tran.queue = self.__queue(tsec[t]['queue'])
      tran.security = self.__security(tsec[t]['Security'])
      trans[t] = tran
    return trans

  def __sensors(self,cfg):
    pass

  def __sensor_handlers(self):
    snsec = self.__cfg['Sensors']
    handelers = {}
    for sh in snsec:
      if snsec[sh]['type'] == 'virtual':
        for sns in snsec[sh]:
          pass
      elif snsec[sh]['type'] == '1wire/usb':
        pass
      elif snsec[sh]['type'] == 'adc/beagleboneblack':
        pass

  def __data(self):
    datas = {}
    dsec = self.__cfg['Data']
    for d in dsec:
      if dsec[d]['format'] == 'sense.xml':
        data = SenseDataHandler()
        data.identifier = self._identity(dsec[d]['Identification'])
        datas[d] = data
      else:
        pass #todo error?

    return datas"""

#Taken from
# http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
  def _load_obj(self,name):
    components = name.split('.')
    path = '.'.join(components[:-1])
    clss = components[-1:][0]
    mod = __import__(path,globals(),locals(),clss)
    return getattr(mod,clss)()

  def _set_args(self,obj,key,value):
    if value.strip()[0] == '$':
      #delay evaluation
      pass
    else:
      arg = ast.literal_eval(value)
      logging.debug('Setting attribute %s to %s for class %s' % (key,arg,obj))
      setattr(obj,key,arg)



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
            print('You want a named variable: '+ c + ' (with type' + tp + ')')
            print('ltsense.{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            #self._object_map[c] = self._load_obj('{0}.{1}'.format(section.lower(),self.types[section][cfg[c]['type']]))
            self.proc(cfg[c],section,c)
        else:
          print("You want a attribute: " + c + " for " + variable )
          #Anything starting with $ or is a list has delayed evaluation
          if cfg[c][0] == '$' or isinstance(cfg[c],list):
            print("Delay eval for" +  cfg[c])
            self._delayed_eval[variable] = cfg[c]
          elif c != 'type':
            pass
          else:
            self._set_args(self._object_map[variable],c,cfg[c])
            #print('You want a ' + self.types[c][cfg[c]['type']])


  def __init__(self, filename):

    cfg = ConfigObj(filename)

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
              'Sensors' :
                  { 'virtual' : 'handlers.GeneralSensorHandler' ,
                    '1wire/usb' : 'handlers.OWFSSensorHandler' }
            }


    self.proc(cfg)



