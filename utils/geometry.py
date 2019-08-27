import numpy as np


def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return r, phi


def polar_to_cartesian(r, phi):
    rad_p = phi * np.pi / 180.
    x = r * np.cos(rad_p)
    y = r * np.sin(rad_p)
    return x, y
