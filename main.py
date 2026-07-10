import cv2
import time

from src.camera import Camera
from src.background import BackgroundManager
from src.hand_tracker import HandTracker
from src.portal import Portal
from src.gestures import GestureRecognizer


def main():

    # -----------------------------
    # Initialize
    # -----------------------------

    camera = Camera()

    bg_manager = BackgroundManager()

    tracker = HandTracker()

    gesture = GestureRecognizer()

    portal = Portal()

    # -----------------------------
    # Capture Background
    # -----------------------------

    if not bg_manager.capture(camera):

        print("Background Capture Failed")

        return

    print("\nAI Magic Portal Started Successfully\n")

    # -----------------------------
    # Variables
    # -----------------------------

    current_gesture = "NONE"

    prev_time = time.time()

    fps = 0

    # -----------------------------
    # Main Loop
    # -----------------------------

    while True:

        frame = camera.read()

        if frame is None:
            break

        current_gesture = "NONE"

        hand = tracker.detect(frame)

        if hand:

            portal.update(

                hand["x"],
                hand["y"],
                hand["radius"]

            )

            current_gesture = gesture.recognize(

                hand["landmarks"]

            )

            # -----------------------------
            # Gesture Controls
            # -----------------------------

            if current_gesture == "OPEN":

                portal.increase_size()

            elif current_gesture == "FIST":

                portal.decrease_size()

            elif current_gesture == "OK":

                portal.next_theme()

        frame = portal.draw(

            frame,
            bg_manager.get_background()

        )

                # -----------------------------
        # FPS
        # -----------------------------

        current_time = time.time()

        fps = int(
            1 / (current_time - prev_time + 0.0001)
        )

        prev_time = current_time

        # -----------------------------
        # Professional HUD
        # -----------------------------

        cv2.putText(
            frame,
            "AI Magic Portal v2.0",
            (20, 35),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Gesture : {current_gesture}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 200, 255),
            2
        )

        cv2.putText(
            frame,
            "Move your hand to control the portal",
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "B : Capture Background",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "T : Change Theme",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Q : Quit",
            (20, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # -----------------------------
        # Show Window
        # -----------------------------

        cv2.imshow(
            "AI Magic Invisibility Portal",
            frame
        )

        # -----------------------------
        # Keyboard
        # -----------------------------

        key = cv2.waitKey(1) & 0xFF

        if key == ord("b"):

            bg_manager.capture(camera)

        elif key == ord("t"):

            portal.next_theme()

        elif key == ord("q"):

            break
            # -----------------------------
    # Cleanup
    # -----------------------------

    tracker.close()

    camera.release()

    cv2.destroyAllWindows()


# -----------------------------
# Run Program
# -----------------------------

if __name__ == "__main__":

    main()