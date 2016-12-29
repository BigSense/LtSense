from ltsense.sensors import AbstractSensor
import logging
import sys

class AbstractOwfsSensor(AbstractSensor):

    def __init__(self, ow_sensor):
        AbstractSensor.__init__(self)
        try:
            import ow
        except ImportError:
            logging.error('1-Wire Python Module not found. Did you install python-ow?')
            sys.exit(8)
        self.ow_sensor = ow_sensor
        self.id = ow_sensor.id


class TemperatureSensor(AbstractOwfsSensor):

    def __init__(self, ow_sensor):
        AbstractOwfsSensor.__init__(self, ow_sensor)
        self.units = 'C'
        self.type = 'Temperature'

    def _read_temp(self):
        return self.ow_sensor.temperature.strip()

    data = property(_read_temp, lambda self, v: None)
