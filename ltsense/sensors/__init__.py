#!/usr/bin/env python


## --- Base Classes --##

class SensorReadException(Exception):
  """Exception generated during a read error from any sensor. Designed to
     be caught in the Transport layer."""

  def __init__(self, value):
    Exception.__init__(self)
    self.value = value

  def __str__(self):
    return repr(self.value)

class AbstractSensor(object):
  """Base for all Sensors to Extend"""

  def __init__(self):
    object.__init__(self)
    self.id = 'Unimplemented'
    self.type = 'Unimplemented'
    self.data = 'Unimplemented'
    self.units = 'Unimplemented'