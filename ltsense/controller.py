#!/usr/bin/env python

from threading import Thread
import time
import ltsense
import logging
import sys


class AbstractController(Thread):

    def __init__(self):
        Thread.__init__(self)

        self.sample_rate = 10.0
        self.transports = None
        self.sensor_handlers = []
        self.data_handler = None

    def run(self):
        while not ltsense.exit_all_threads:
            self.process_sensor_data()
            time.sleep(float(self.sample_rate))
        logging.info('Exit Detected. Stopping Controller Thread')

    def process_sensor_data(self):
        sensors = []
        for h in self.sensor_handlers:
            # if not in a list, put in a list and extend (TODO: place in a helper library?)
            if h.sensors is not None:
                sensors.extend([h.sensors] if type(h.sensors) == str else h.sensors)

        data = self.data_handler.render_data(sensors)

        for t in self.transports:
            t.send_package(data)


class DefaultController(AbstractController):

    def __init__(self):
        AbstractController.__init__(self)


class RespawningController(AbstractController):

    def __init__(self):
        AbstractController.__init__(self)
        # default, exit if we respawn more than 10
        # times in 10 seconds
        self.respawn_rate_limit = 10
        self.respawn_time_limit = 10

    def run(self):
        spawn_count = 0
        spawn_time = int(time.time())

        try:
            AbstractController.run()
        except:
            logging.error('Main Process Loop Generated an Exception: %s' % sys.exc_info()[0])
