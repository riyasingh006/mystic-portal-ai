import math


class PortalAnimation:

    def __init__(self):

        self.angle = 0.0
        self.time = 0.0

    def update(self):

        # Portal Rotation Speed
        self.angle += 2.5

        if self.angle >= 360:
            self.angle -= 360

        self.time += 0.08

    def get_angle(self):

        return self.angle

    def get_scale(self):

        # Smooth breathing animation
        return 1.0 + 0.05 * math.sin(self.time * 2.5)