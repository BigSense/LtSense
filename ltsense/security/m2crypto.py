__author__ = 'Sumit Khanna <sumit@penguindreams.org>'

from M2Crypto import EVP, RSA
from ltsense.security import DataSecurity
from os import path
import logging
import base64

class SignatureSecurity(DataSecurity):

  def __init__(self):
    DataSecurity.__init__(self)
    self.ready = False
    self.keyFile = 'key.pem'
    self.keySize = 2048


  def initalize_security(self):
    if self.dataDir != None:
      if not path.isdir(self.dataDir):
        logging.error('Security Data Directory does not exist or is not a directory: %s' % self.dataDir)
      else:
        keyPath = path.join(self.dataDir,self.keyFile)

        if path.isfile(keyPath):
          logging.info("Loading existing keys from %s. PEM: %s" % (self.dataDir,self.keyFile))
          self._key = EVP.load_key(keyPath)
          self.ready = True
        else:
          logging.info("No keys found. Generating New Keys")
          #TODO magic strings and such
          self._key = RSA.gen_key(self.keySize, 65537)
          self._key.save_pem(keyPath, cipher=None)
          self.ready = True

  def sign_data(self,data):
    self._key.reset_context(md='sha1')
    self._key.sign_init()
    self._key.sign_update(data)
    return base64.b64encode(self._key.sign_final())