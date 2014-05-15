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
    self.transports = None
    self.identifier = None
    self._security = None

  def render_data(self,sensors):
    pass

  def _init_security(self,security):
    self._security = security
    security.initalize_security()

  security = property(lambda self : self._security,lambda self,value:self._init_security(value) )

  def transport_data(self,payload):
    if self.transports is not None:
      for t in self.transports:
        t.send_package(payload)
   

class AgraDataHandler(AbstractDataHandler):

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
    if self._security != None:
      signature = self._security.sign_data(doc.toxml())
      logging.info("Data Signature: " + signature)
  
    self.transport_data(
      ("%s\n\n%s" % (doc.toxml(),signature)) if self.security != None else doc.toxml()
    )



