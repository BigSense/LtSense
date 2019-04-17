from ltsense.sensors import AbstractSensor
import logging
import time

class MCP3008(AbstractSensor):

    # Software SPI configuration:
    # CLK  = 18
    # MISO = 23
    # MOSI = 24
    # CS   = 25

    def __init__(self):
        AbstractSensor.__init__()
        self.spi_port = None
        self.spi_device = None
        self.channel = None
        self.__mcp = None
        try:
            import Adafruit_GPIO.SPI as SPI
            #import Adafruit_MCP3008
        except ImportError:
            logging.error('Adafruit MCP3008 module not found')
            sys.exit(8)

        # Software SPI
        # self.mcp = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS, miso=self.MISO, mosi=self.MOSI)

    def _read_data(self):
        if self.spi_port is not None and self.spi_device is not None and self.channel is not None:
            if self.__mcp is None:
                self.__mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.spi_port, self.spi_device))
            # Data can be collected
            return str(self.__mpc.read_adc(self.channel))
        else:
            return None

    data = property(_read_data, lambda self, v: None)

    model = property(lambda self: self._model, _select_phidget)
