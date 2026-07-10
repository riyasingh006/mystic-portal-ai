import cv2
import numpy as np


class Distortion:

    def __init__(self):
        pass

    def apply(self, image, center, radius):

        h, w = image.shape[:2]

        overlay = image.copy()

        # Soft Glow Circle
        cv2.circle(
            overlay,
            center,
            radius + 12,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Very light distortion effect
        output = cv2.addWeighted(
            overlay,
            0.08,
            image,
            0.92,
            0
        )

        return output