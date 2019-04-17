#!/usr/bin/env python3
# Author: Sumit Khanna<sumit@penguindreams.org>
# https://bigsense.io
# Copyright 2019
#
# License: GNU GPLv3

import unittest
import json

from ltsense.data import SenseJsonDataHandler
from ltsense.identifier import NamedIdentifier
from ltsense.sensors.virtual import VirtualTemperatureSensor
from ltsense.location import VirtualLocation


class SenseJsonDataHandlerTest(unittest.TestCase):

    def setUp(self):
        self.vtemp = VirtualTemperatureSensor()
        self.vtemp.id = 'TempUnitTest1'
        self.vtemp.range_min = 5
        self.vtemp.range_max = 5

        ident = NamedIdentifier()
        ident.id = 'UnitTestID'
        self.data_handler = SenseJsonDataHandler()
        self.data_handler.identifier = ident

    def tearDown(self):
        pass

    def test_render_sensor_data_no_gps(self):
        rendered = json.loads(self.data_handler.render_data([self.vtemp]))
        self.assertEqual(len(rendered), 1)
        self.assertEqual(rendered[0]['id'], 'UnitTestID')
        self.assertEqual(len(rendered[0]['sensors']), 1)
        self.assertEqual(rendered[0]['sensors'][0]['id'], 'TempUnitTest1')
        self.assertEqual(rendered[0]['sensors'][0]['type'], 'Temperature')
        self.assertEqual(rendered[0]['sensors'][0]['units'], 'C')
        self.assertEqual(rendered[0]['sensors'][0]['data'], '5')
        #self.assertEqual(json, '[{"id": "UnitTestID", "timestamp": "1552661229958", "sensors": [{"id": "TempUnitTest1", "type": "Temperature", "units": "C", "data": "5"}]}]')

    def test_rendor_sensor_data_some_gps(self):
        l = VirtualLocation()
        l.longitude = '123.567'
        l.latitude = '987.432'
        l.altitude = '6243'
        l.speed = '126kph'
        l.climb = '24.987'
        l.track = '54.323'
        self.data_handler.location = l
        rendered = json.loads(self.data_handler.render_data([self.vtemp]))
        self.assertEqual(rendered[0]['id'], 'UnitTestID')
        self.assertEqual(len(rendered[0]['sensors']), 1)
        self.assertEqual(rendered[0]['sensors'][0]['id'], 'TempUnitTest1')
        self.assertEqual(rendered[0]['sensors'][0]['type'], 'Temperature')
        self.assertEqual(rendered[0]['sensors'][0]['units'], 'C')
        self.assertEqual(rendered[0]['sensors'][0]['data'], '5')
        self.assertEqual(rendered[0]['location']['longitude'], '123.456')

    def test_rendor_sensor_data_all_gps(self):
        pass
