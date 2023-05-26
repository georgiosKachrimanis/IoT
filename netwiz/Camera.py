
class Camera:
    @staticmethod
    def check_camera():
        try:
            camera = picamera.PiCamera()
            camera.close()
            return True
        except picamera.PiCameraError:
            return False

    def __init__(self):
        if not Camera.check_camera():
            raise RuntimeError("No camera detected.")

        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)

    def start(self):
        self.stream = io.BytesIO()
        self.camera.start_recording(self.stream, format='h264', quality=23)

    def stop(self):
        self.camera.stop_recording()
        self.stream.close()

    def get_frame(self):
        self.stream.seek(0)
        return self.stream.read()
