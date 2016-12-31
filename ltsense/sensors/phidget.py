from ltsense.sensors import AbstractSensor
import logging
import math
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.InterfaceKit import InterfaceKit


class PhidgetSensor(AbstractSensor):

    def __init__(self):
        AbstractSensor.__init__(self)
        # Can be analogue or digital
        self.port_type = None
        self.port_num = None
        self.current_data = None
        self.id = None
        self.data_formula = None
        self._model = None

    def _select_phidget(self, model_number):
        model_init = {
            # Precision Light Sensor
            '1127': {'type': 'Light',
                     'units': 'lux',
                     'data': lambda x: x},
            # Sound Sensor
            '1133': {'type': 'Sound',
                     'units': 'dB',
                     'data': lambda x: 16.801 * math.log(x) + 9.872},
            # Absolute Air Pressure Sensor (20-400 kPa)
            '1140': {'type': 'Air Pressure',
                     'units': 'kPa',
                     'data': lambda x: (x / 2.421) + 3.478}
        }.get(model_number)
        self.type = model_init['type']
        self.units = model_init['units']
        self.data_formula = model_init['data']
        self._model = model_number

    def _read_data(self):
        if self.current_data is None or self.data_formula is None:
            return None
        else:
            return str(self.data_formula(self.current_data))

    data = property(_read_data, lambda self, v: None)

    model = property(lambda self: self._model, _select_phidget)
