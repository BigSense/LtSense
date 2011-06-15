#!/usr/bin/env python

import sqlite3
import time
from xml.dom.minidom import Document

class AbstractDataHandler():

  def __init__(self):
    pass
    
  def render_data(self,sensors):
    pass

class SQLiteDataHandler(AbstractDataHandler):
  
  def __init__(self):
    AbstractDataHandler.__init__(self)   
    self.__conn = None


  def set_file(self,dataFile):
    self.sqlFile = dataFile
    self.__get_cursor().execute("CREATE TABLE IF NOT EXISTS sensor_data (stamp DATETIME,type TEXT, sensor_id Text,date Text)")
    self.__conn.commit()


  def __get_cursor(self):
    try:
      if self.__conn == None:
        self.__conn = sqlite3.connect(self.sqlFile)
      return self.__conn.cursor()
    except sqlite3.ProgrammingError:
      self.__conn = sqlite3.connect(self.sqlFile)
      return self.__conn.cursor()

  def render_data(self,sensors):
    now = time.time()
    for s in sensors:
      self.__get_cursor().execute(
        'INSERT INTO sensor_data VALUES(?,?,?,?)' , (now,s.get_type(),s.get_id(),s.get_data())
        )
      self.__conn.commit()

class GreenOvenDataHandler(AbstractDataHandler):

  def __init__(self):
    AbstractDataHandler.__init__(self)
 
  def set_endpoint(self,hostname):
    self.__remote_host = hostname

  def render_data(self,sensors):
    now = time.time()
    doc = Document()
    root = doc.createElement('GreenData')

    ts = doc.createElement('timestamp')
    ts.setAttribute('zone','UTC')
    ts.appendChild(doc.createTextNode(str(time.time())))

    sens = doc.createElement('Sensors')

    for s in sensors:
      senNode = doc.createElement('Sensor')

      did = doc.createElement('id')
      dtype = doc.createElement('type')
      dunits = doc.createElement('units')
      ddata = doc.createElement('data')

      did.appendChild(doc.createTextNode(s.get_id()))
      dtype.appendChild(doc.createTextNode(s.get_type()))
      dunits.appendChild(doc.createTextNode(s.get_units()))
      ddata.appendChild(doc.createTextNode(s.get_data()))
 
      senNode.appendChild(did)
      senNode.appendChild(dtype)
      senNode.appendChild(dunits)
      senNode.appendChild(ddata)
      sens.appendChild(senNode)

    root.appendChild(ts)
    root.appendChild(sens)
    doc.appendChild(root)
    print doc.toprettyxml(indent=' ')

class WaterMLDataHandler(AbstractDataHandler):
 
  def __init__(self,conifg):
    AbstractDataHandler.__init__(self,config)
    
  def render_data(self,sensors):
    pass

