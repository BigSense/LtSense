#!/usr/bin/env python

import time
from xml.dom.minidom import Document
import logging
import ltsense


class AbstractDataHandler(object):

    def __init__(self):
        object.__init__(self)
        self.identifier = None

    def render_data(self, sensors):
        pass


class SenseDataHandler(AbstractDataHandler):

    def __init__(self):
        AbstractDataHandler.__init__(self)

    def render_data(self, sensors):
        doc = Document()
        root = doc.createElement('AgraData')

        pack = doc.createElement('package')
        # Webservice expects time as a long in miliseconds.
        # time.time() is seconds as a float
        pack.setAttribute("timestamp", "%d" % round(time.time() * 1000))
        pack.setAttribute("id", self.identifier.identify())

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
