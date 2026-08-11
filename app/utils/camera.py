import cv2 

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    def read_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Failed to read frame from camera.")
        return frame

    def release(self):
        cv2.destroyAllWindows()
        self.camera.release()