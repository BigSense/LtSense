#!/usr/bin/env python

from Queue import Queue
from threading import Thread
import time
import urllib2
import logging
import sys

class AbstractTransport:
  
  def __init__(self):
    pass
  
  def send_package(self,payload):
    pass


class QueuedHttpPostTransport(AbstractTransport,Thread):
  
  def __init__(self):

    self.__queue = None
    self.pause_rate = 0.010
    self.url = None

    AbstractTransport.__init__(self)
    Thread.__init__(self)
    self.__queue = Queue()
    self.start()

  def run(self):       
    while(True):
      payload = self.__queue.get()
      try:
        response = urllib2.urlopen(self.url,payload)
        time.sleep(float(self.pause_rate))
      except (urllib2.HTTPError,urllib2.URLError) as err:
        msg = err.code if isinstance(err,urllib2.HTTPError) else err.reason
        logging.warn('Error delivering payload: %s. Requeueing (Queue Size:%d)' % (msg,self.__queue.qsize()))
        self.__queue.put(payload)
      except:
        logging.error('Unknown exception %s. Requeueing (Queue Size:%d)' % (sys.exc_info()[0],self.__queue.qsize()))
        self.__queue.put(payload)

  def send_package(self,payload):
    self.__queue.put(payload)
