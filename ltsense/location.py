#!/usr/bin/env/python

from threading import Thread
from gps import gps, WATCH_ENABLE
import logging
import time

class AbstractLocation(object):

    def __init__(self):
        object.__init__(self)
        self.location_ready = False
        self.x = 0
        self.y = 0
        self.accuracy = 0
        self.altitude = 0


    def location(self):
        """
        Returns a dictionary with {x, y, accuracy, altitude} or None.
        This should return immediately. Population of GPS data
        should occur in a seperate thread. 
        """
        if not self.location_ready:
            return None
        else:
            return { 'x': self.x, 'y': self.y, 'accuracy': self.accuracy, 'altitude': self.altitude }


class VirtualLocation(AbstractLocation):

    def __init__(self):
        self.location_ready = True


class GPSLocation(AbstractLocation, Thread):

    def __init__(self):
        AbstractLocation.__init__(self)
        Thread.__init__(self)
        self._gps = gps(mode=WATCH_ENABLE)
        self.location_ready = False
        self.poll_rate = 1.0
        self.start()
        logging.info("GPS Location Thread Activated")

    def run(self):
        try:
            while True:
                report = self._gps.next()
                # Wait for a 3D Fix
                if report['class'] == 'TPV' and report['mode'] == 3:
                    self.x = str(report.lon)
                    self.y = str(report.lat)
                    self.altitude = str(report.alt)
                    self.accuracy = str(1)
                    self.location_ready = True
                time.sleep(self.poll_rate)
        except StopIteration:
            logging.error('GPS Thread Stopped')
            self.location_ready = False
