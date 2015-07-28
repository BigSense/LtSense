#!/usr/bin/env python

import time
from xml.dom.minidom import Document
import logging
import ltsense


class AbstractDataHandler(object):

    def __init__(self):
        object.__init__(self)
        self.identifier = None
        self.location = None

    def render_data(self, sensors):
        pass


class SenseDataHandler(AbstractDataHandler):

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
        # Webservice expects time as a long in miliseconds.
        # time.time() is seconds as a float
        pack.setAttribute("timestamp", "%d" % round(time.time() * 1000))
        pack.setAttribute("id", self.identifier.identify())

        # Location
        if self.location is not None:
            gps = self.location.location()
            if gps is not None:
                xml_gps = doc.createElement('gps')

                for section, attrs in {
                  'location': ['longitude', 'latitude', 'altitude'],
                  'delta': ['speed', 'track', 'climb'],
                  'accuracy': ['longitude_error', 'latitude_error',
                    'altitude_error', 'speed_error', 'climb_error', 'track_error']
                }.iteritems():
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
