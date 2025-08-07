# translator/camera.py
import cv2

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if success:
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None
