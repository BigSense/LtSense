#!/usr/bin/env/python


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


class GPSLocation(AbstractLocation):

    def __init__(self):
        #TODO: start thread to connect to GPS daemon
        pass