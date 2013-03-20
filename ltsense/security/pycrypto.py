__author__ = 'Sumit Khanna <sumit@penguindreams.org'

#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from os import path
from os import urandom
import logging

class SignatureSecurity(DataSecurity):

  def __init__(self):
    DataSecurity.__init__(self)
    self.ready = False
    self.privateKeyFile = 'key'
    self.publicKeyFile = 'key.pub'
    self.keySize = 2048

  def initalize_security(self):
    if self.dataDir != None:
      if not path.isdir(self.dataDir):
        logging.error('Security Data Directory does not exist or is not a directory: %s' % self.dataDir)
      else:

        priPath = path.join(self.dataDir,self.privateKeyFile)
        pubPath = path.join(self.dataDir,self.publicKeyFile)

        if path.isfile(priPath) and path.isfile(pubPath):
          logging.info("Loading existing keys from %s. Public: %s / Private: %s" % (self.dataDir,self.publicKeyFile,self.privateKeyFile))
          with open(priPath,'r') as fpri:
            self.__private_key = fpri.read()
          with open(pubPath,'r') as fpub:
            self.__public_key = fpub.read()
          self.__key = RSA.importKey(self.__private_key)
          self.ready = True
        else:
          logging.info("No keys found. Generating New Keys")
          # private_key is a string suitable for storing on disk for retrieval later
          # public_key is a string suitable for sending to the server
          # The server should store this along with the client ID for verification
          self.__key = RSA.generate(self.keySize,urandom)
          self.__private_key = self.__key.exportKey()
          self.__public_key = self.__key.publickey().exportKey()
          with open(pubPath,'w') as fpub:
            logging.info("Writing Public Key to %s" % pubPath)
            fpub.write(self.__public_key)
          with open(priPath,'w') as fpri:
            logging.info("Writing Private Key to %s" % priPath)
            fpri.write(self.__private_key)
          self.ready = True


  def sign_data(self,data):
    if self.ready == True:
      logging.debug('Data to sign: "%s"' % data)
      digest = SHA.new(data.strip()).digest()
      logging.debug('Digest: "%s"' % repr(digest))
      return str(self.__key.sign(digest, None)[0])
    return ''


