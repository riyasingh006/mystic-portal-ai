import cv2
import numpy as np


class Portal:

    def __init__(self, radius=120):
        self.x = 320
        self.y = 240
        self.radius = radius

    # -------------------------
    # Smooth Position Update
    # -------------------------
    def update(self, x, y):

        speed = 0.18

        self.x = int(self.x + (x - self.x) * speed)
        self.y = int(self.y + (y - self.y) * speed)

    # -------------------------
    # Smooth Radius Update
    # -------------------------
    def set_radius(self, radius):

        radius = max(60, min(180, radius))

        speed = 0.20

        self.radius = int(
            self.radius + (radius - self.radius) * speed
        )

    # -------------------------
    # Draw Portal
    # -------------------------
    def draw(self, frame, background):

        h, w = frame.shape[:2]

        # Circle Mask
        mask = np.zeros((h, w), dtype=np.uint8)

        cv2.circle(
            mask,
            (self.x, self.y),
            self.radius,
            255,
            -1
        )

        # Soft Edge
        mask = cv2.GaussianBlur(mask, (15, 15), 4)

        alpha = mask.astype(np.float32) / 255.0
        alpha = cv2.merge([alpha, alpha, alpha])

# Match brightness of captured background to current frame
        bg = background.copy()

        result = (
            frame.astype(np.float32) * (1 - alpha)
            + bg.astype(np.float32) * alpha
        )

        result = result.astype(np.uint8)

        # Glow
        glow = result.copy()

        for r in range(self.radius + 8, self.radius + 36, 8):

            cv2.circle(
                glow,
                (self.x, self.y),
                r,
                (255, 180, 0),
                2,
                cv2.LINE_AA
            )

        result = cv2.addWeighted(
            glow,
            0.30,
            result,
            0.70,
            0
        )

        # Main Ring
        cv2.circle(
            result,
            (self.x, self.y),
            self.radius,
            (0, 255, 255),
            3,
            cv2.LINE_AA
        )

        cv2.circle(
            result,
            (self.x, self.y),
            self.radius - 4,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Center Crosshair
        cv2.line(
            result,
            (self.x - 10, self.y),
            (self.x + 10, self.y),
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.line(
            result,
            (self.x, self.y - 10),
            (self.x, self.y + 10),
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        return result