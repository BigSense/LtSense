#!/usr/bin/env python

from Queue import Queue
from threading import Thread
import time
import urllib2
import logging
import sys

class AbstractTransport(object):
  
  def __init__(self):
    object.__init__(self)
  
  def send_package(self,payload):
    pass


class QueuedHttpPostTransport(AbstractTransport,Thread):
  
  def __init__(self):

    self.__queue = None
    self.pause_rate = 0.10
    self.timeout = 10.0
    self.url = None

    AbstractTransport.__init__(self)
    Thread.__init__(self)
    self.__queue = Queue()
    self.start()

  def run(self):       
    while(True):
      payload = self.__queue.get()
      try:

        logging.debug('Preparing payload for transport %s' % payload)
        response = urllib2.urlopen(self.url,payload)
        logging.debug('Payload transported')

        time.sleep(float(self.pause_rate))
      except (urllib2.HTTPError,urllib2.URLError) as err:
        msg = err.code if isinstance(err,urllib2.HTTPError) else err.reason
        logging.warn('Error delivering payload: %s. Requeueing (Queue Size:%d). Retry in %d' % (msg,self.__queue.qsize(),self.timeout))
        self.__queue.put(payload)
        time.sleep(float(self.timeout))
      except:
        logging.error('Unknown exception %s. Requeueing (Queue Size:%d). Retry in %d' % (sys.exc_info()[0],self.__queue.qsize(),self.timeout))
        self.__queue.put(payload)
        time.sleep(float(self.timeout))

  def send_package(self,payload):
    self.__queue.put(payload)
