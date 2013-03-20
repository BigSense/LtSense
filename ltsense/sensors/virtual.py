from ltsense.sensors import AbstractSensor
import random
import os 
import base64

#### --- Testing / Fake Sensors --- ####

class StaticInformationSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.id = "Unimplemented"
    self.type = "Unimplemented"
    self.data = "Unimplemented"
    self.units = "Unimplemented"


class RandomSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.rangeMin = 0
    self.rangeMax = 10

  def _random(self):
    return str(random.randint(int(self.rangeMin),int(self.rangeMax)))

  data = property(_random,lambda self,v:None )


class ImageSensor(AbstractSensor):

  def __init__(self):
    AbstractSensor.__init__(self)
    self.id = 'UnknownVirtualCamera'
    self.type = 'Image'
    self.units = 'NImageU' #Non-Comissioned Photo Units
    self._imageFile = ''
    self._image = None

  def _set_image(self,pfile):
    self._imageFile = pfile
    fd = open(pfile,'rb')
    self._image = fd.read()
    fd.close()
    
  def _get_mime64_image(self):
    return base64.b64encode(self._image)

  data = property(_get_mime64_image,lambda self,v:None)
  imageFile = property(lambda self: self._imageFile,_set_image)


class IncrementingSensor(AbstractSensor):
  
  def __init__(self):
    AbstractSensor.__init__(self)
    self.rangeMin = 0
    self.rangeMax = 10
    self.current = -1
    self.countDir = None
    self.float = False
    self.floatPercision = 2      
    
  def _read_vcount(self):
    
    cfile = os.path.join(self.countDir,self.id)
    
    if self.current == -1:
      if os.path.exists(cfile):
        fd = open(cfile,'r')
        self.current = fd.readlines()[0].strip()
        fd.close()
      else:
        self.current = 0
    
    if bool(self.float):
      self.current = ('%.'+self.floatPercision+'f') % (float(self.current) + random.uniform(float(self.rangeMin),float(self.rangeMax)))
      
    else :
      self.current = int(self.current) + random.randint(int(self.rangeMin),int(self.rangeMax))
      
    fd = open(cfile,'w')
    fd.write(str(self.current))
    fd.close
    return str(self.current)
    
  data = property(_read_vcount,lambda self,v:None )  