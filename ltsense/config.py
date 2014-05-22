#!/usr/bin/env python
from configobj import ConfigObj
from ltsense.data import SenseDataHandler
from ltsense.identification import MacAddressIdentifier,UUIDIdentifier,NamedIdentifier
from ltsense.queue import MemoryQueue, SQLiteQueue
from ltsense.security.m2crypto import M2Security
from ltsense.security.pypiRsa import RSASecurity
from ltsense.transport.http import QueuedHttpPostTransport


class BootStrap(object):

  def _identity(self,idsec):
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

  def __sensors(self):
    snsec = self.__cfg['Sensors']
    senses = {}
    for s in senses:
      if senses[s]['type'] == 'virtual':
        pass
      elif senses[s]['type'] == '1wire/usb':
        pass
      elif senses[s]['type'] == 'adc/beagleboneblack':
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

    return datas




  def __init__(self, filename):

    cfg = ConfigObj(filename)

    dev_id = self.__identify(cfg)
    for sns in cfg['Sensors']:
      stype = sns['type']


    cfg['General']['sample_rate']

