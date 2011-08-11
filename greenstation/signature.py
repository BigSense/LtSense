#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from os import path
import logging

class AbstractSecurity(object):
  
  def __init__(self):
    object.__init__(self)
    self.dataDir = None
    
  def initalize_security(self):
    pass

  def sign_data(self,data):
    return 'Unimplemented'

  def encrypt_data(self,data):
    return 'Unimplemented'

class SignatureSecurity(AbstractSecurity):

  def __init__(self):
    AbstratSecurity.__init__(self)
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
	  self.__private_key = RSA.importKey(priPath)
	  with open(pubPath,'r') as fpub:
	    self.__public_key = fpub.read()
	  self.ready = True
	else:
          # private_key is a string suitable for storing on disk for retrieval later
          # public_key is a string suitable for sending to the server
          # The server should store this along with the client ID for verification
          key = RSA.generate(self.keySize)
          self.__private_key = key.exportKey()
          self.__public_key = key.publickey().exportKey()
          with open(pubPath,'w') as fpub:
	    fpub.write(self.__public_key)
	  with open(priPath,'w') as fpri:
	    fpri.write(self.__private_key)
          self.ready = True


  def sign_data(self,data):
    if self.ready = True:
      digest = SHA.new(data).digest()
      return self.__private_key.sign(digest, None)
    return ''
