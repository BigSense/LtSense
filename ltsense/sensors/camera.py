from ltsense.sensors import AbstractSensor, SensorReadException
#from ltsense.capture import Camera
import base64

"""TODO: probably need to get rid of this. It was really just for those
non-standard web cams"""

"""
# --- Camera/Photo Sensors --- #

class ImageSensor(AbstractSensor):
  
  def __init__(self):
    AbstractSensor.__init__(self)
    self.id = 'UnknownCamera'
    self.type = 'Image'
    self.units = 'NImageU' #Non-Comissioned Photo Units
    self.resolution = '640x480'
    self.mode = 'mjpg'
    self.device = '/dev/video0'
    
    #We have to wait for dependency injection from the loader.py
    # to change the defaults above before we init the camera,
    # so we'll do it in the _capture_photo function 
    self.__camera = None
    
  def _capture_photo(self):
    try:
      
      if self.__camera == None:
        self.__camera = Camera(mode=self.mode,resolution=self.resolution,device=self.device)
      
      return base64.b64encode( self.__camera.grab_frame() )
    except capture.error as err:
      raise SensorReadException('Error reading camera: %s' % err)
      
  data = property(_capture_photo,lambda self,v:None)
  """
