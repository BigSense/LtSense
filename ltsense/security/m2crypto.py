__author__ = 'Sumit Khanna <sumit@penguindreams.org>'

from M2Crypto import EVP, RSA
from ltsense.security import DataSecurity
from os import path
import logging
import base64

class M2Security(DataSecurity):

  def __init__(self):
    DataSecurity.__init__(self)


  def initalize_security(self):
    if self.data_dir is not None:
      if not path.isdir(self.data_dir):
        logging.error('Security Data Directory does not exist or is not a directory: %s' % self.data_dir)
      else:
        key_path = path.join(self.data_dir,self.key_file)

        if path.isfile(key_path):
          logging.info("Loading existing keys from %s. PEM: %s" % (self.data_dir,self.key_file))
          self._key = EVP.load_key(key_path)
          self.ready = True
        else:
          logging.info("No keys found. Generating New Keys")
          #TODO magic strings and such
          self._key = RSA.gen_key(self.key_size, 65537)
          self._key.save_pem(key_path, cipher=None)
          self.ready = True

  def sign_data(self,data):
    self._key.reset_context(md='sha1')
    self._key.sign_init()
    self._key.sign_update(data)
    return base64.b64encode(self._key.sign_final())