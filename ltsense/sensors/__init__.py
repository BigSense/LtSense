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


class AbstractOneWireSensor(AbstractSensor):
  """Reads and writes commands from Agranet command line application.
     Issues a read and thorws exception on error message. This class
     will be replaced with a native Python module eventually. For now,
     the extProc member must be set to an ExternalProcessHandler"""
  
  def __init__(self,unique_id,extProc):
    AbstractSensor.__init__(self)
    self.id = unique_id
    self.extProc = extProc

  def _read_data(self):
    "Issues a read for the Sensor'd id property and returns the numeric result"
    
    #multi sensors have a - and their distinct type (FlowRate/Volume)
    #  I hate doing it this way, but spliting on '-' and [0] works
    self.extProc.write_line('get %s' % self.id.split('-')[0])
    value =  self.extProc.read_line()
    if value.strip() == 'DEVICE_READ_FAIL' or value.strip() == 'NO_SUCH_DEVICE':
      raise SensorReadException('Could not read %s. Error: %s' % (self.id,value))
    else:
      return value

  data = property(_read_data,lambda self,v:None)

