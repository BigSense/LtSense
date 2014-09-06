from ltsense.sensors import AbstractSensor
import ow

class AbstractOwfsSensor(AbstractSensor):

  def __init__(self,ow_sensor):
    AbstractSensor.__init__(self)
    self.ow_sensor = ow_sensor

  def _ow_id(self):
    return self.ow_sensor.id

  id = property(_ow_id, lambda self, v:None)


class TemperatureSensor(AbstractOwfsSensor):

  def __init__(self,ow_sensor):
    AbstractOwfsSensor.__init__(self,ow_sensor)
    self.units = 'C'
    self.type='Temperature'


  def _read_temp(self):
    return self.ow_sensor.temperature.strip()

  data = property(_read_temp,lambda self,v:None )