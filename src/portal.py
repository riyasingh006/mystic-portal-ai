import cv2

from src.utils import (
    smooth,
    clamp,
    create_circle_mask,
    alpha_blend,
    draw_glow,
    draw_ring,
    draw_rotating_portal,
    draw_energy_arcs,
    draw_fire_edge
)

from src.effects import Effects
from src.particles import ParticleSystem
from src.distortion import Distortion
from src.animation import PortalAnimation
from src.themes import Theme


class Portal:

    def __init__(self):

        self.x = 640
        self.y = 360
        self.radius = 120

        self.effects = Effects()
        self.particles = ParticleSystem()
        self.distortion = Distortion()
        self.animation = PortalAnimation()
        self.theme = Theme()

    # -----------------------------
    # Update
    # -----------------------------

    def update(self, x, y, radius):

        self.x = smooth(
            self.x,
            x,
            0.18
        )

        self.y = smooth(
            self.y,
            y,
            0.18
        )

        radius = clamp(
            radius,
            80,
            220
        )

        self.radius = smooth(
            self.radius,
            radius,
            0.20
        )

    # -----------------------------
    # Gesture Controls
    # -----------------------------

    def increase_size(self):

        self.radius = min(
            250,
            self.radius + 8
        )

    def decrease_size(self):

        self.radius = max(
            60,
            self.radius - 8
        )

    def next_theme(self):

        self.theme.next()

    # -----------------------------
    # Draw Portal
    # -----------------------------

    def draw(self, frame, background):

        if background is None:
            return frame

        cx = int(self.x)
        cy = int(self.y)

        self.animation.update()

        r = int(
            self.radius *
            self.animation.get_scale()
        )

        theme = self.theme.get()

        if background.shape[:2] != frame.shape[:2]:

            background = cv2.resize(
                background,
                (
                    frame.shape[1],
                    frame.shape[0]
                )
            )

        # Portal Mask

        mask = create_circle_mask(
            frame.shape,
            (cx, cy),
            r,
            blur=71
        )

        # Invisibility

        output = alpha_blend(
            frame,
            background,
            mask
        )

        # Glow

        output = draw_glow(
            output,
            (cx, cy),
            r
        )

        # Ring

        output = draw_ring(
            output,
            (cx, cy),
            r,
            theme["ring"]
        )

        # -----------------------------
        # Doctor Strange Portal
        # -----------------------------

        output = draw_rotating_portal(
            output,
            (cx, cy),
            r,
            self.animation.get_angle(),
            theme["ring"]
        )

        # -----------------------------
        # Energy Arcs
        # -----------------------------

        output = draw_energy_arcs(
            output,
            (cx, cy),
            r,
            self.animation.get_angle(),
            theme["ring"]
        )

        # -----------------------------
        # Fire Edge
        # -----------------------------

        output = draw_fire_edge(
            output,
            (cx, cy),
            r,
            self.animation.get_angle(),
            theme["particle"]
        )

        # -----------------------------
        # Distortion
        # -----------------------------

        output = self.distortion.apply(
            output,
            (cx, cy),
            r
        )

        # -----------------------------
        # Magic Aura
        # -----------------------------

        output = self.effects.apply(
            output,
            (cx, cy),
            r
        )

        # -----------------------------
        # Magic Particles
        # -----------------------------

        output = self.particles.update(
            output,
            (cx, cy),
            r
        )

        # -----------------------------
        # Crosshair
        # -----------------------------

        cv2.line(
            output,
            (cx - 12, cy),
            (cx + 12, cy),
            theme["ring"],
            2,
            cv2.LINE_AA
        )

        cv2.line(
            output,
            (cx, cy - 12),
            (cx, cy + 12),
            theme["ring"],
            2,
            cv2.LINE_AA
        )

        # -----------------------------
        # Center Dot
        # -----------------------------

        cv2.circle(
            output,
            (cx, cy),
            4,
            (255, 255, 255),
            -1,
            cv2.LINE_AA
        )

        return output