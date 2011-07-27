#!/usr/bin/env python

from Queue import Queue
from threading import Thread
import time
import urllib2

class AbstractTransport:
  
  def __init__(self):
    pass
  
  def send_package(self,payload):
    pass


class QueuedHttpPostTransport(AbstractTransport,Thread):
  
  __queue = None
  pause_rate = 0.010
  url = None

  def __init__(self):
    AbstractTransport.__init__(self)
    Thread.__init__(self)
    self.__queue = Queue()
    self.start()

  def run(self):
    while(True):
      payload = self.__queue.get()
      #TODO: Try/Catch/requeue
      response = urllib2.urlopen(self.url,payload)
      time.sleep(float(self.pause_rate))

  def send_package(self,payload):
    self.__queue.put(payload)
