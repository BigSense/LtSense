#!/usr/bin/env python
from configobj import ConfigObj
from ltsense.identification import MacAddressIdentifier,UUIDIdentifier,NamedIdentifier
from ltsense.queue import MemoryQueue, SQLiteQueue
from ltsense.security.m2crypto import M2Security
from ltsense.security.pypiRsa import RSASecurity
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
      return None

  def __queue(self,config):
      if config['type'] == 'memory':
        return MemoryQueue()
      elif config['type'] == 'sqlite':
        q = SQLiteQueue()
        q.data_file = config['data']
        return q
      else:
        return None

  def __security(self,config):
    s = None
    if config['type'] == "rsa":
      s = RSASecurity()
    elif config['type'] == "m2":
      s = M2Security()
    elif config['type'] == "none":
      s = None

    if s is None:
      return None
    else:
      s.data_dir = config['data_dir']
      s.key_file = config['key_file']
      s.key_size = config['key_size']
      return s

  def __transports(self):
    tsec = self.__cfg['Transports']
    for t in tsec:
      trans = QueuedHttpPostTransport()
      trans.url = t['url']
      trans.format = t['format']
      trans.pause_rate = t['pause_rate']
      trans.queue = self.__queue(t['queue'])
      trans.security = self.__security(t['Security'])

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

