#!/usr/bin/env python

from Queue import Queue
from threading import Thread
import time
import urllib2
import logging
import sys
import greenstation

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
    self.queue_timeout = 1.0
    self.url = None

    AbstractTransport.__init__(self)
    Thread.__init__(self)
    self.__queue = Queue()
    self.start()

  def run(self):   
   
    while not greenstation.exit_all_threads:
      
      try:
        #use a queue_timeout in case exit_all_threads
        # is set to True, we don't want to block forever
        payload = self.__queue.get(self.queue_timeout)
      except Empty as empty:
        contine 
        
      try:
        logging.debug('Preparing payload for transport %s' % payload)
        response = urllib2.urlopen(self.url,payload)
        logging.debug('Payload transported')

        time.sleep(float(self.pause_rate))
      except (urllib2.HTTPError,urllib2.URLError) as err:
        msg = err.code if isinstance(err,urllib2.HTTPError) else err.reason
        logging.warn('Error delivering payload: %s. Requeueing (Queue Size:%s). Retry in %s' % (msg,self.__queue.qsize(),self.timeout))
        self.__queue.put(payload)
        time.sleep(float(self.timeout))
      except:
        logging.error('Unknown exception %s. Requeueing (Queue Size:%s). Retry in %s' % (sys.exc_info()[0],self.__queue.qsize(),self.timeout))
        self.__queue.put(payload)
        time.sleep(float(self.timeout))
        
    logging.info('Exit Detected. Stopping Transport Thread')

  def send_package(self,payload):
    self.__queue.put(payload)
