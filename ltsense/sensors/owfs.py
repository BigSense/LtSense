from ltsense.sensors import AbstractSensor


class AbstractOwfsSensor(AbstractSensor):

    def __init__(self, ow_sensor):
        AbstractSensor.__init__(self)
        import ow
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
