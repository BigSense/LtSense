#!/usr/bin/env/python

from threading import Thread
from gps import gps, WATCH_ENABLE
import logging
import time
import ltsense

class AbstractLocation(object):

    def __init__(self):
        object.__init__(self)
        self.location_ready = False
        self.longitude = 0
        self.latitude = 0
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
            return { 'longitude': self.longitude, 'latitude': self.latitude, 'accuracy': self.accuracy, 'altitude': self.altitude }


class VirtualLocation(AbstractLocation):

    def __init__(self):
        self.location_ready = True


class GPSLocation(AbstractLocation, Thread):

    def __init__(self):
        AbstractLocation.__init__(self)
        Thread.__init__(self)
        self._gps = gps(mode=WATCH_ENABLE)
        self.location_ready = False
        self.poll_rate = 0.3
        self.start()
        logging.info("GPS Location Thread Activated")

    def run(self):
        try:
            while not ltsense.exit_all_threads:
                report = self._gps.next()
                # Wait for a 3D Fix
                if report['class'] == 'TPV' and report['mode'] == 3:
                    self.longitude = str(report.lon)
                    self.latitude = str(report.lat)
                    self.altitude = str(report.alt)
                    self.accuracy = str(1)
                    if not self.location_ready:
                        logging.info('GPS 3D Lock Acquired')
                    self.location_ready = True
                # We've lost our GPS fix. Stop adding Location info
                elif report['class'] == 'TPV' and report['mode'] != 3:
                    if self.location_ready:
                        logging.info('GPS 3D Lock Lost')    
                    self.location_ready = False                
                time.sleep(self.poll_rate)
        except StopIteration:
            logging.error('GPS Thread Stopped')
            self.location_ready = False
