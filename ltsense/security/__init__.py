#!/usr/bin/env python
__author__ = 'Sumit Khanna <sumit@penguindreams.org>'

class DataSecurity(object):

  def __init__(self):
    object.__init__(self)
    self.dataDir = None
    self.siteName = 'Unknown'

  def initalize_security(self):
    pass

  def sign_data(self,data):
    return 'Unimplemented'

  def encrypt_data(self,data):
    return 'Unimplemented'