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
    self.key_file = 'key.pem'
    self.key_size = 2048
    self._key = None

  def initalize_security(self):
    if self.data_dir is not None:
      if not path.isdir(self.data_dir):
        logging.error('Security Data Directory does not exist or is not a directory: %s' % self.data_dir)
      else:
        key_path = path.join(self.data_dir,self.key_file)

        if path.isfile(key_path):
          logging.info("Loading existing keys from %s. PEM: %s" % (self.data_dir,self.key_file))
          with open(key_path,'rb') as fd:
            self._key = rsa.PrivateKey.load_pkcs1(fd.read())
          self.ready = True
        else:
          logging.info("No keys found. Generating New Keys")
          (pubkey, privkey) = rsa.newkeys(self.key_size)
          pem = rsa.PrivateKey.save_pkcs1(privkey)
          with open(key_path,'wb') as fd:
            fd.write(pem)

          #reread the file we just wrote
          with open(key_path) as fd:
            self._key = rsa.PrivateKey.load_pkcs1(fd.read())

  def sign_data(self,data):
    return base64.b64encode(rsa.sign(data,self._key,'SHA-1')).decode('UTF-8')