#!/usr/bin/env python

class AbstractTransport:
  
  def send_package(self,data):
    pass


class BasicHttpTransport(AbstractTransport):
  pass

class QueuedHttpTransport(AbstractTransport):
  pass
