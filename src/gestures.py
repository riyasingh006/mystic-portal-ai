import math


class GestureRecognizer:

    def __init__(self):
        self.current = "NONE"

    def recognize(self, landmarks):

        if landmarks is None:
            self.current = "NONE"
            return self.current

        # Required landmarks
        thumb = landmarks[4]
        index = landmarks[8]
        middle = landmarks[12]
        ring = landmarks[16]
        pinky = landmarks[20]

        wrist = landmarks[0]

        # Finger state
        index_up = index.y < landmarks[6].y
        middle_up = middle.y < landmarks[10].y
        ring_up = ring.y < landmarks[14].y
        pinky_up = pinky.y < landmarks[18].y

        # Thumb distance
        d = math.hypot(index.x - thumb.x, index.y - thumb.y)

        # -------------------------
        # Open Palm
        # -------------------------
        if index_up and middle_up and ring_up and pinky_up:

            self.current = "OPEN"

        # -------------------------
        # Fist
        # -------------------------
        elif (not index_up and
              not middle_up and
              not ring_up and
              not pinky_up):

            self.current = "FIST"

        # -------------------------
        # Victory
        # -------------------------
        elif index_up and middle_up and not ring_up and not pinky_up:

            self.current = "VICTORY"

        # -------------------------
        # OK
        # -------------------------
        elif d < 0.05:

            self.current = "OK"

        # -------------------------
        # Point
        # -------------------------
        elif index_up and not middle_up:

            self.current = "POINT"

        else:

            self.current = "UNKNOWN"

        return self.current
    
    