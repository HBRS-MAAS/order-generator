import numpy as np


def location(pos):
    x, y = np.round(pos, 2)
    return {'x': x, 'y': y}

