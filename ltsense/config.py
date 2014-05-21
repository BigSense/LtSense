#!/usr/bin/env python
from configobj import ConfigObj
from ltsense.identification import MacAddressIdentifier,UUIDIdentifier,NamedIdentifier
from ltsense.queue import MemoryQueue, SQLiteQueue
from ltsense.security.m2crypto import M2Security
from ltsense.transport.http import QueuedHttpPostTransport


class BootStrap(object):

  def __identity(self):
    idsec = self.__cfg['Identification']
    if idsec['type'] == "name":
      return NamedIdentifier(idsec['name'])
    elif idsec['type'] == "mac":
      return MacAddressIdentifier(idsec['adapter'])
    elif idsec['type'] == "uuid":
      return UUIDIdentifier(idsec['file'])
    else:
      #todo error
      exit(3)

  def __queue(self,config):
      if config['type'] == 'memory':
        return MemoryQueue()
      elif config['type'] == 'sqlite':
        q = SQLiteQueue()
        q.data_file = config['data']
        return q

  def __transports(self):
    tsec = self.__cfg['Transports']
    for t in tsec:
      trans = QueuedHttpPostTransport()
      trans.url = t['url']
      trans.format = t['format']
      trans.pause_rate = t['pause_rate']
      trans.queue = self.__queue(t['queue'])
      if t['Security']['type'] == "rsa":
        pass
      elif t['Security']['type'] == "m2":
        s = M2Security()
        s.key_file = t['Security']['key']
        trans.security = s
      elif t['Security']['type'] == "none":
        trans.security = None


  def __data(self):
    datas = {}
    for dt in self.__cfg['Data']:
      if dt['format'] == 'sense.xml':
        pass
      else:
        pass #todo error?




  def __init__(self, filename):

    cfg = ConfigObj(filename)

    dev_id = self.__identify(cfg)
    for sns in cfg['Sensors']:
      stype = sns['type']


    cfg['General']['sample_rate']

