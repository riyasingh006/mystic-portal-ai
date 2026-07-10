import cv2
import random
import math


class Particle:

    def __init__(self, center, radius):

        self.reset(center, radius)

    def reset(self, center, radius):

        self.angle = random.uniform(0, 360)

        self.radius = radius

        self.distance = random.uniform(
            radius - 8,
            radius + 8
        )

        self.speed = random.uniform(
            1.5,
            3.5
        )

        self.life = random.randint(
            40,
            80
        )

        self.size = random.randint(
            2,
            4
        )

        self.update(center)

    def update(self, center):

        self.angle += self.speed

        r = self.distance + random.uniform(-2, 2)

        self.x = center[0] + math.cos(
            math.radians(self.angle)
        ) * r

        self.y = center[1] + math.sin(
            math.radians(self.angle)
        ) * r

        self.life -= 1

    def draw(self, image):

        if self.life <= 0:
            return

        color = random.choice([
            (255, 120, 0),
            (255, 170, 0),
            (255, 220, 50),
            (255, 255, 255)
        ])

        cv2.circle(
            image,
            (int(self.x), int(self.y)),
            self.size,
            color,
            -1,
            cv2.LINE_AA
        )


class ParticleSystem:

    def __init__(self):

        self.particles = []

    def update(self, image, center, radius):

        while len(self.particles) < 80:

            self.particles.append(
                Particle(center, radius)
            )

        alive = []

        for particle in self.particles:

            particle.update(center)

            particle.draw(image)

            if particle.life > 0:

                alive.append(particle)

            else:

                alive.append(
                    Particle(center, radius)
                )

        self.particles = alive

        return image