#!/usr/bin/env python

class AbstractDataHandler():

  def __init__(self,config):
    pass
    
  def render_data(self,sensors):
    pass

class SQLiteDataHandler(AbstractDataHandler):
  
  def __init__(self,config):
    AbstractDataHandler.__init__(self,config)    

  def render_data(self,sensors):
    for s in sensors:
      print(s.get_data())

class WaterMLDataHandler(AbstractDataHandler):
 
  def __init__(self,conifg):
    AbstractDataHandler.__init__(self,config)
    
  def render_data(self,sensors):
    pass

