#!/usr/bin/env python
from configobj import ConfigObj
from ltsense.identification import MacAddressIdentifier,UUIDIdentifier,NamedIdentifier
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

  def __queue(self):


  def __transports(self):
    tsec = self.__cfg['Transports']
    for t in tsec:
      trans = QueuedHttpPostTransport()
      trans.url = t['url']
      trans.format = t['format']
      trans.pause_rate = t['pause_rate']

      q = t['queue']
      if q['type'] == 'memory':




  def __init__(self, filename):

    cfg = ConfigObj(filename)

    dev_id = self.__identify(cfg)
    for sns in cfg['Sensors']:
      stype = sns['type']


    cfg['General']['sampleRate']

