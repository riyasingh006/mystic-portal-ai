import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        if results.multi_hand_landmarks is None:
            return None

        hand = results.multi_hand_landmarks[0]

        self.drawer.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )

        h, w = frame.shape[:2]

        # Index Finger Tip
        index = hand.landmark[8]

        # Thumb Tip
        thumb = hand.landmark[4]

        x = int(index.x * w)
        y = int(index.y * h)

        tx = int(thumb.x * w)
        ty = int(thumb.y * h)

        radius = int(math.hypot(x - tx, y - ty) * 2)

        radius = max(80, min(radius, 220))

        # Draw Portal Center
        cv2.circle(
            frame,
            (x, y),
            8,
            (0, 255, 0),
            -1
        )

        return {
            "x": x,
            "y": y,
            "radius": radius,
            "index": (x, y),
            "thumb": (tx, ty),
            "landmarks": hand.landmark
        }

    def close(self):

        self.hands.close()