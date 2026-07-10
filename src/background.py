import cv2
import time


class BackgroundManager:

    def __init__(self):
        self.background = None

    def capture(self, camera, countdown=3):

        print("\n==============================")
        print(" Stand away from the camera ")
        print("==============================")

        # Countdown
        for i in range(countdown, 0, -1):

            frame = camera.read()

            if frame is not None:

                text = f"Capturing in {i}"

                cv2.putText(
                    frame,
                    text,
                    (350, 80),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1.3,
                    (0, 255, 255),
                    3
                )

                cv2.imshow(
                    "AI Magic Invisibility Portal",
                    frame
                )

                cv2.waitKey(1)

            time.sleep(1)

        background = None

        # Capture stable background
        for _ in range(30):

            frame = camera.read()

            if frame is not None:
                background = frame.copy()

        if background is None:

            print("Background Capture Failed")
            return False

        self.background = background

        print("Background Captured Successfully")

        return True

    def get_background(self):

        return self.background

    def has_background(self):

        return self.background is not None

    def reset(self):

        self.background = None