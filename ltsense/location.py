#!/usr/bin/env/python

from threading import Thread
import logging
import time
import ltsense

class AbstractLocation(object):

    def __init__(self):
        object.__init__(self)
        self.location_ready = False
        self.longitude = ''
        self.latitude = ''
        self.altitude = ''
        self.speed = ''
        self.climb = ''
        self.track = ''
        self.longitude_error = ''
        self.latitude_error = ''
        self.altitude_error = ''
        self.speed_error = ''
        self.climb_error = ''
        self.track_error = ''


    def location(self):
        """
        Returns a dictionary with {longitude, latitude, altitude,
        speed, climb, track, longitude_error, latitude_error,
        altitude_error, speed_error, climb_error,
        track_error} or None.
        This should return immediately. Population of GPS data
        should occur in a seperate thread.
        """
        if not self.location_ready:
            return None
        else:
            return { 'longitude': self.longitude, 'latitude': self.latitude,
                     'altitude': self.altitude, 'speed': self.speed,
                     'climb': self.climb, 'track': self.track,
                     'longitude_error': self.longitude_error,
                     'latitude_error': self.latitude_error,
                     'altitude_error': self.altitude_error,
                     'speed_error': self.speed_error,
                     'climb_error': self.climb_error,
                     'track_error': self.track_error }


class VirtualLocation(AbstractLocation):

    def __init__(self):
        AbstractLocation.__init__(self)
        self.location_ready = True


class GPSLocation(AbstractLocation, Thread):

    def __init__(self):
        from gps import gps, WATCH_ENABLE
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
                    self.longitude = str(report.lon) if 'lon' in report else ''
                    self.latitude = str(report.lat) if 'lat' in report else ''
                    self.altitude = str(report.alt) if 'alt' in report else ''
                    self.speed = str(report.speed) if 'speed' in report else ''
                    self.track = str(report.track) if 'track' in report else ''
                    self.climb = str(report.climb) if 'climb' in report else ''
                    self.longitude_error = str(report.epx) if 'epx' in report else ''
                    self.latitude_error = str(report.epy) if 'epy' in report else ''
                    self.altitude_error = str(report.epv) if 'epv' in report else ''
                    self.speed_error = str(report.eps) if 'eps' in report else ''
                    self.climb_error = str(report.epc) if 'epc' in report else ''
                    self.track_error = str(report.epd) if 'epd' in report else ''
                    if not self.location_ready:
                        logging.info('GPS 3D Lock Acquired')
                    self.location_ready = True
                # We've lost our GPS fix. Stop adding Location info
                elif report['class'] == 'TPV' and report['mode'] != 3:
                    if self.location_ready:
                        logging.info('GPS 3D Lock Lost (Mode:{})'.format(report['mode']))
                    self.location_ready = False
                time.sleep(self.poll_rate)
        except StopIteration:
            logging.error('GPS Thread Stopped')
            self.location_ready = False
