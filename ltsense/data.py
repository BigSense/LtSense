#!/usr/bin/env python

import time
from xml.dom.minidom import Document
import logging
import ltsense
import json


class AbstractDataHandler(object):

    def __init__(self):
        object.__init__(self)
        self.identifier = None
        self.location = None
        self.gps_fields = {'location': ['longitude', 'latitude', 'altitude'],
                           'delta': ['speed', 'track', 'climb'],
                           'accuracy': ['longitude_error', 'latitude_error',
                                        'altitude_error', 'speed_error',
                                        'climb_error', 'track_error']}

    def render_data(self, sensors):
        pass

    def timestamp(self):
        # Webservice expects time as a long in miliseconds.
        # time.time() is seconds as a float
        return int(round(time.time() * 1000))


class SenseJsonDataHandler(AbstractDataHandler):

    def __init__(self):
        AbstractDataHandler.__init__(self)

    def render_data(self, sensors):

        data = {'id': self.identifier.identify(),
                'timestamp': str(self.timestamp())}
        # Location
        if self.location is not None:
            loc_info = {}
            gps = self.location.location()
            if gps is not None:
                for section, attrs in self.gps_fields.iteritems():
                    loc_section = {}
                    for a in attrs:
                        loc_section[a] = gps[a]
                    loc_info[section] = loc_section
                data['gps'] = loc_info

        sensor_data = []
        for s in sensors:
            sensor_data.append({'id': s.id,
                                'type': s.type,
                                'units': s.units,
                                'data': s.data})

        data['sensors'] = sensor_data
        # LtSense only sends single packages, but BigSense
        # can accept multiple packages with both XML and JSON
        data = [data]
        logging.debug('Generated JSON {}'.format(json.dumps(data, indent=2)))
        return json.dumps(data)


class SenseXMLDataHandler(AbstractDataHandler):

    def __init__(self):
        AbstractDataHandler.__init__(self)

    def _gps_block(self, doc, name, attributes, gps):
        node = doc.createElement(name)
        for a in attributes:
            node.setAttribute(a, gps[a])
        return node

    def render_data(self, sensors):
        doc = Document()
        root = doc.createElement('sensedata')

        pack = doc.createElement('package')
        pack.setAttribute("timestamp", '{0:d}'.format(self.timestamp()))
        pack.setAttribute("id", self.identifier.identify())

        # Location
        if self.location is not None:
            gps = self.location.location()
            if gps is not None:
                xml_gps = doc.createElement('gps')
                for section, attrs in self.gps_fields.iteritems():
                    xml_gps.appendChild(self._gps_block(doc, section, attrs, gps))

                pack.appendChild(xml_gps)

        sens = doc.createElement('sensors')

        err = []

        for s in sensors:
            sen_node = doc.createElement('sensor')
            sen_node.setAttribute('id', s.id)
            sen_node.setAttribute('type', s.type)
            sen_node.setAttribute('units', s.units)

            ddata = doc.createElement('data')

            try:
                ddata.appendChild(doc.createTextNode(s.data))
            except ltsense.sensors.SensorReadException as e:
                err.append(e.value)

            sen_node.appendChild(ddata)
            sens.appendChild(sen_node)

        pack.appendChild(sens)

        # errors
        err_list = None
        if len(err) > 0:
            err_list = doc.createElement('errors')
        for e in err:
            err_node = doc.createElement('error')
            err_node.appendChild(doc.createTextNode(e))
            err_list.appendChild(err_node)
        if err_list is not None:
            pack.appendChild(err_list)

        root.appendChild(pack)
        doc.appendChild(root)
        logging.debug('Generated XML\n' + doc.toprettyxml())

        # Data Signature
        return doc.toxml()
