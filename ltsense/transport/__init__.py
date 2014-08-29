#!/usr/bin/env python

from Queue import Queue, Empty
from threading import Thread
import time
import logging
import sys
import ltsense

#--Base Classes--

class AbstractTransport(object):
  """Base class for all transport handlers. It's not very useful to 
  extend this class directly. It's better to extend the QueuedTransport"""
  
  def __init__(self):
    object.__init__(self)
    self._security = None

  def send_package(self,payload):
    if self._security is not None:
      signature = self._security.sign_data(payload)
      logging.info("Data Signature: " + signature)
      return "%s\n\n%s" % (payload,signature)
    else:
      return payload

  def _init_security(self,security):
    if self._security is not None:
      self._security = security
      security.initalize_security()

  security = property(lambda self : self._security,lambda self,value:self._init_security(value) )


    
class QueuedTransport(AbstractTransport,Thread):
  """Base class for all transports that which to use a queueing system.
  The send_package() function is implemented and a new abstract function,
  _run_transport() need to be implemented in the subclass to transport the 
  data."""

  def __init__(self):

    self.pause_rate = 0.10
    self.timeout = 10.0
    self.queue = None

    AbstractTransport.__init__(self)
    Thread.__init__(self)
    self.start()

  def run(self):   
    """Main thread to handle queue. In most cases, this function
    should not need to be overridden."""

    while not ltsense.exit_all_threads:

      #Because of the way dependency injection works in the loader.py,
      # the queue may not be set when the thread is started on initilization, 
      # so we must way for the queue to be set.
      if self.queue is None:
        logging.info('Queue Not Initalized Yet. Waiting...')
        time.sleep(float(self.pause_rate))
        continue;

      payload = self.queue.dequeue()
      if payload is None:
        continue
        
      try:
        if self._run_transport(payload):
          logging.debug('Payload transported. (Queue Size: %s)' % self.queue.size)
          time.sleep(float(self.pause_rate)) 
        else:
          logging.warn('Error delivering payload. Requeueing (Queue Size:%s). Retry in %s' % (self.queue.size,self.timeout))
          self.queue.enqueue(payload)
          time.sleep(float(self.timeout))   
      except:
        logging.error('Unknown exception %s. Requeueing (Queue Size:%s). Retry in %s' % (sys.exc_info()[0],self.queue.size,self.timeout))
        self.queue.enqueue(payload)
        time.sleep(float(self.timeout))     
   
    logging.info('Exit Detected. Stopping Transport Thread')

  def send_package(self,payload):
    """Adds the payload to the queue which is handeled by the queue thread."""
    payload = AbstractTransport.send_package(payload)
    self.queue.enqueue(payload)

  def _run_transport(self,payload):
    """Implement this function in subclasses to transport data. 
    Return false if the data failed to transport so it will be 
    placed back in the queue."""
    logging.warn('Unimplemented Queue Transport Detected. You have tried to use an abstract class. Did you want QueuedHttpPostTransport?')
    return True