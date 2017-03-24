from ltsense.sensors import AbstractSensor
import base64
import logging

class CV2Camera(AbstractSensor):

    def __init__(self):
        AbstractSensor.__init__(self)
        from cv2 import cv
        self.type = 'Photo'
        self.units = 'jpeg'
        # TODO configurable camera port
        self._camera = cv.CaptureFromCAM(0)
        # Ramp up images
        logging.debug('Ramping up Camera')
        # TODO configure ramp up
        for i in xrange(30):
            cv.QueryFrame(self._camera)

    def _photo_base64(self):
        from cv2 import cv
        import cv2
        import numpy
        img = cv.QueryFrame(self._camera)
        return base64.b64encode(cv.EncodeImage('.jpg', img).tostring())

    data = property(_photo_base64, lambda self, v: None)
