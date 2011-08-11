#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

class Security(object):
  
  def __init__(self):
    object.__init__(self)
    self.dataDir = None
    
  def 


from Crypto.PublicKey import RSA
key = RSA.generate(2048)
private_key = key.exportKey()
public_key = key.publickey().exportKey()
# private_key is a string suitable for storing on disk for retrieval later
# public_key is a string suitable for sending to the server
# The server should store this along with the client ID for verification



key = RSA.importKey(private_key)
# where private_key is read from wherever you stored it previously
digest = SHA.new(message).digest()
signature = key.sign(digest, None)
# attach signature to the message however you wish
