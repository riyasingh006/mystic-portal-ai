import cv2
import math
import time


class Effects:

    def __init__(self):

        self.start_time = time.time()

    def draw_energy(
        self,
        image,
        center,
        radius
    ):

        t = time.time() - self.start_time

        overlay = image.copy()

        for i in range(6):

            angle = t * 180 + i * 60

            r = radius + int(
                8 * math.sin(t * 3 + i)
            )

            color = (
                255,
                min(255, 120 + i * 20),
                20
            )

            cv2.ellipse(
                overlay,
                center,
                (r, r),
                angle,
                0,
                360,
                color,
                2,
                cv2.LINE_AA
            )

        return cv2.addWeighted(
            overlay,
            0.45,
            image,
            0.55,
            0
        )

    def draw_aura(
        self,
        image,
        center,
        radius
    ):

        overlay = image.copy()

        for i in range(20):

            color = (
                255,
                max(0, 180 - i * 6),
                0
            )

            cv2.circle(
                overlay,
                center,
                radius + i * 3,
                color,
                1,
                cv2.LINE_AA
            )

        return cv2.addWeighted(
            overlay,
            0.25,
            image,
            0.75,
            0
        )

    def apply(
        self,
        image,
        center,
        radius
    ):

        image = self.draw_aura(
            image,
            center,
            radius
        )

        image = self.draw_energy(
            image,
            center,
            radius
        )

        return image