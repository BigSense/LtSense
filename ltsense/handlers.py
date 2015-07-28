# --- Sensor Handlers --- #
from ltsense.sensors.owfs import TemperatureSensor
import logging

class AbstractSensorHandler(object):

    def __init__(self):
        object.__init__(self)
        self.sensors = []


class OWFSSensorHandler(AbstractSensorHandler):

    def __init__(self):
        AbstractSensorHandler.__init__(self)
        # Avoid a direct dependency
        import ow
        ow.init('u')

    def _sensors(self):
        import ow
        sensors = []
        try:
            for s in ow.Sensor('/').sensorList():
                if s.family == '28' or s.family == '10':
                     sensors.append(TemperatureSensor(s))
            return sensors
        except ow.exUnknownSensor as e:
            logging.warn('Error Reading 1-Wire: {}'.format(e))

    sensors = property(_sensors, lambda self, v: None)


class GeneralSensorHandler(AbstractSensorHandler):

    def __init__(self):
        AbstractSensorHandler.__init__(self)
