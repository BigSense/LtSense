__author__ = 'Sumit Khanna <sumit@penguindreams.org>'

from ltsense.security import DataSecurity
import logging
from os import path
import rsa
import base64

class RSASecurity(DataSecurity):

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
          with open(keyPath,'rb') as fd:
            self._key = rsa.PrivateKey.load_pkcs1(fd.read())
          self.ready = True
        else:
          logging.info("No keys found. Generating New Keys")
          (pubkey, privkey) = rsa.newkeys(self.keySize)
          pem = rsa.PrivateKey.save_pkcs1(privkey)
          with open(keyPath,'wb') as fd:
            fd.write(pem)

          #reread the file we just wrote
          with open(keyPath) as fd:
            self._key = rsa.PrivateKey.load_pkcs1(fd.read())

  def sign_data(self,data):
    return base64.b64encode(rsa.sign(data,self._key,'SHA-1')).decode('UTF-8')