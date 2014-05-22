#!/usr/bin/env python

#import sqlite3
import time
from xml.dom.minidom import Document
import fcntl, socket, struct 
import logging
import ltsense

class AbstractDataHandler(object):

  def __init__(self):
    object.__init__(self)
    self.identifier = None

  def render_data(self,sensors):
    pass

class SenseDataHandler(AbstractDataHandler):

  def __init__(self):
    AbstractDataHandler.__init__(self)

  def render_data(self,sensors):
    doc = Document()
    root = doc.createElement('AgraData')

    pack = doc.createElement('package')
    #Webservice expects time as a long in miliseconds. 
    #time.time() is seconds as a float
    pack.setAttribute("timestamp", "%d" % round(time.time()* 1000) )
    pack.setAttribute("id",self.identifier.identify())

    sens = doc.createElement('sensors')

    err = []

    for s in sensors:
      senNode = doc.createElement('sensor')

      senNode = doc.createElement('sensor')
      senNode.setAttribute('id',s.id)
      senNode.setAttribute('type',s.type)
      senNode.setAttribute('units',s.units)

      ddata = doc.createElement('data')
      
      try:
        ddata.appendChild(doc.createTextNode(s.data))
      except ltsense.sensors.SensorReadException as e:
        err.append(e.value)
 
      senNode.appendChild(ddata)
      sens.appendChild(senNode)

    pack.appendChild(sens)
    
    #errors
    if len(err) > 0:
      errList = doc.createElement('errors')
    for e in err:
      errNode = doc.createElement('error')
      errNode.appendChild(doc.createTextNode(e))
      errList.appendChild(errNode)
    pack.appendChild(errList)
    

    root.appendChild(pack)  
    doc.appendChild(root)
    logging.debug('Generated XML\n' + doc.toprettyxml())
    
    #Data Signature
    return doc.toxml()




