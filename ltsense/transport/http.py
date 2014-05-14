#!/usr/bin/env python


import urllib2
import logging
from ltsense.transport import QueuedTransport


class QueuedHttpPostTransport(QueuedTransport):
  
  def __init__(self, url = None):
    self.url = url
    QueuedTransport.__init__(self)

  def _run_transport(self,payload):      
      try:
        logging.debug('Preparing payload for transport to %s' % self.url)
        urllib2.urlopen(self.url,payload)
        return True
      except (urllib2.HTTPError,urllib2.URLError) as err:
        msg = err.code if isinstance(err,urllib2.HTTPError) else err.reason
        logging.error('HTTP Error %s' % msg)        
        return False
