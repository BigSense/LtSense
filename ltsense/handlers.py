# --- Sensor Handlers --- #
from ltsense.sensors.owfs import TemperatureSensor, HumiditySensor
import logging


class AbstractSensorHandler(object):

    def __init__(self):
        object.__init__(self)
        self.sensors = []


class PhidgetSensorHandler(AbstractSensorHandler):

    def __init__(self):
        self.device = None
        self._attach_timeout = None
        self._data_rate = None
        self._sensors = None

    def _try_init(self):
        if all([self._data_rate, self._attach_timeout, self._sensors]):
            try:
                from Phidgets.Devices.InterfaceKit import InterfaceKit
                from Phidgets.PhidgetException import PhidgetException
                self.interface_kit = InterfaceKit()
                self.interface_kit.setOnAttachHandler(lambda e: self._attach(e))
                self.interface_kit.setOnDetachHandler(lambda e: self._detach(e))
                self.interface_kit.setOnErrorhandler(lambda e: self._error(e))
                self.interface_kit.setOnSensorChangeHandler(lambda e: self._sensor_change(e))
                self.interface_kit.openPhidget()
                self.interface_kit.waitForAttach(self._attach_timeout)
                for i in range(self.interface_kit.getSensorCount()):
                    self.interface_kit.setDataRate(i, self._data_rate)
                logging.info("Phidget Sensor Handler Initalized")
                for s in self._sensors:
                    if s.port_num is not None:
                        s.current_data = self.interface_kit.getSensorValue(s.port_num)
                        logging.debug("Setting Initial Value for Sensor {} to {}".format(s.port_num, s.current_data))
                    else:
                        logging.warn("Cannot set Initial Value for Sensor {}".format(s.port_num))
            except ImportError:
                self.interface_kit = None
                logging.error('Phidget Python Module not found. Did you install python-phidget?')
            except PhidgetException as e:
                self.interface_kit = None
                logging.error("Could not Initalize Phidget Kit: {}".format(e.details))

    def _read_sensors(self):
        ready_sensors = []
        for s in self._sensors:
            if s.data is not None:
                ready_sensors.append(s)
        return ready_sensors

    def _set_sensors(self, v):
        logging.debug('Adding Phidget Sensors :: {}'.format(v))
        self._sensors = v
        self._try_init()

    sensors = property(_read_sensors, _set_sensors)

    attach_timeout = property(lambda self: self._attach_timeout,
                              lambda self, v: self._set_config('attach_timeout', v))

    data_rate = property(lambda self: self._data_rate,
                         lambda self, v: self._set_config('data_rate', v))

    def _set_config(self, prop, value):
        if prop == 'data_rate':
            self._data_rate = value
        elif prop == 'attach_timeout':
            self._attach_timeout = value
        self._try_init()

    def _attach(self, e):
        self.device = e.device
        logging.info("Phidget InterfaceKit {} Attached".format(self.device.getSerialNum()))

    def _detach(self, e):
        logging.warn("Phidget InterfaceKit {} Removed".format(e.device.getSerialNum()))
        self.device = None

    def _error(self, e):
        logging.error("Phidget Error {} :: {}".format(e.eCode, e.description))

    def _sensor_change(self, e):
        # logging.debug("Phidget Analog Sensor Change :: Port: {} / Data: {}".format(e.index, e.value))
        for s in self._sensors:
            if s.port_type == 'analog' and s.port_num == e.index:

                # Set a default ID if none given in config file
                if s.id is None:
                    # Default ID is kit serial number::port
                    s.id = '{}:{}:{}'.format(self.device.getSerialNum(),
                                             s.port_type, s.port_num)

                s.current_data = e.value


class OWFSSensorHandler(AbstractSensorHandler):

    def __init__(self):
        AbstractSensorHandler.__init__(self)
        # Avoid a direct dependency
        self.device = 'u'
        self._connected = False

    def _ensure_connect(self):
        import ow
        if not self._connected:
            ow.init(self.device)
            self._connected = True

    def _sensors(self):
        import ow
        self._ensure_connect()
        sensors = []
        try:
            for s in ow.Sensor('/').sensorList():
                if hasattr(s, 'temperature'):
                     sensors.append(TemperatureSensor(s))
                if hasattr(s, 'humidity'):
                    sensors.append(HumiditySensor(s))
            return sensors
        except ow.exUnknownSensor as e:
            logging.warn('Error Reading 1-Wire: {}'.format(e))

    sensors = property(_sensors, lambda self, v: None)


class GeneralSensorHandler(AbstractSensorHandler):

    def __init__(self):
        AbstractSensorHandler.__init__(self)
