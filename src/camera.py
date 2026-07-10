import cv2
import time


class Camera:

    def __init__(self, camera_index=0):

        # Webcam Open
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Cannot open webcam")

        # Camera Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Small Buffer
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        print("Camera Started Successfully")

        # Warm-up Camera
        for _ in range(20):
            self.cap.read()

        time.sleep(0.5)

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        # Mirror Image
        frame = cv2.flip(frame, 1)

        return frame

    def capture_background(self, delay=3):

        print("\n============================")
        print("Stand away from camera")
        print("============================")

        for i in range(delay, 0, -1):
            print(f"Capturing in {i}...")
            time.sleep(1)

        background = None

        for _ in range(30):

            frame = self.read()

            if frame is not None:
                background = frame.copy()

        if background is None:
            raise Exception("Background Capture Failed")

        print("Background Captured Successfully")

        return background

    def release(self):

        if self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()