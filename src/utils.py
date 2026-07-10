import cv2
import numpy as np
import math


# ---------------------------------
# Clamp
# ---------------------------------

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


# ---------------------------------
# Smooth Movement
# ---------------------------------

def smooth(current, target, speed=0.15):
    return current + (target - current) * speed


# ---------------------------------
# Soft Circular Mask
# ---------------------------------

def create_circle_mask(
    shape,
    center,
    radius,
    blur=61
):

    h, w = shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)

    cv2.circle(
        mask,
        center,
        radius,
        255,
        -1
    )

    if blur % 2 == 0:
        blur += 1

    mask = cv2.GaussianBlur(
        mask,
        (blur, blur),
        0
    )

    return mask.astype(np.float32) / 255.0


# ---------------------------------
# Background Blend
# ---------------------------------

def alpha_blend(
    frame,
    background,
    mask
):

    alpha = cv2.merge([
        mask,
        mask,
        mask
    ])

    output = (
        frame.astype(np.float32) * (1 - alpha)
        +
        background.astype(np.float32) * alpha
    )

    return np.clip(
        output,
        0,
        255
    ).astype(np.uint8)

# ---------------------------------
# Portal Glow
# ---------------------------------

def draw_glow(
    image,
    center,
    radius
):

    overlay = image.copy()

    colors = [
        (255, 120, 0),
        (255, 170, 0),
        (255, 220, 50)
    ]

    for i in range(3):

        cv2.circle(
            overlay,
            center,
            radius + 12 + i * 8,
            colors[i],
            2,
            cv2.LINE_AA
        )

    return cv2.addWeighted(
        overlay,
        0.35,
        image,
        0.65,
        0
    )


# ---------------------------------
# Portal Ring
# ---------------------------------

def draw_ring(
    image,
    center,
    radius,
    color=(0, 255, 255)
):

    cv2.circle(
        image,
        center,
        radius,
        color,
        4,
        cv2.LINE_AA
    )

    cv2.circle(
        image,
        center,
        radius - 6,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    return image


# ---------------------------------
# Doctor Strange Portal
# ---------------------------------

def draw_rotating_portal(
    image,
    center,
    radius,
    angle,
    color=(0, 170, 255)
):

    cx, cy = center

    for i in range(24):

        start = int(angle + i * 15)

        cv2.ellipse(
            image,
            (cx, cy),
            (radius, radius),
            0,
            start,
            start + 10,
            color,
            3,
            cv2.LINE_AA
        )

    for i in range(18):

        start = int(-angle + i * 20)

        cv2.ellipse(
            image,
            (cx, cy),
            (radius - 18, radius - 18),
            0,
            start,
            start + 8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    return image

# ---------------------------------
# Energy Arcs
# ---------------------------------

def draw_energy_arcs(
    image,
    center,
    radius,
    angle,
    color
):

    cx, cy = center

    for i in range(8):

        start = int(angle * 2 + i * 45)

        cv2.ellipse(
            image,
            (cx, cy),
            (radius + 8, radius + 8),
            0,
            start,
            start + 18,
            color,
            4,
            cv2.LINE_AA
        )

    return image


# ---------------------------------
# Fire Edge Effect
# ---------------------------------

def draw_fire_edge(
    image,
    center,
    radius,
    angle,
    color
):

    cx, cy = center

    for i in range(80):

        a = math.radians(angle * 2 + i * 4.5)

        r = radius + 10 + 6 * math.sin(
            math.radians(angle * 3 + i * 15)
        )

        x = int(cx + math.cos(a) * r)
        y = int(cy + math.sin(a) * r)

        size = 2 + (i % 3)

        cv2.circle(
            image,
            (x, y),
            size,
            color,
            -1,
            cv2.LINE_AA
        )

    return image