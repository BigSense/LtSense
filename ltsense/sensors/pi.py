from ltsense.sensors import AbstractSensor
import io
import base64

class PiCamera(AbstractSensor):

    def __init__(self):
        AbstractSensor.__init__(self)
        import picamera
        self.type = 'Photo'
        self.units = 'jpeg'
        self._camera = picamera.PiCamera()
        # warm up the camera
        self._camera.start_preview()

    def _photo_base64(self):
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg')
        stream.seek(0)
        base64.b64encode(stream.getvalue())

    data = property(_photo_base64, lambda self, v: None)
