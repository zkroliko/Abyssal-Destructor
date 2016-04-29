import numpy as np

class Area:
    # Sizes
    SIZE_X = 1000.0
    SIZE_Y = 1000.0
    # Values for which the border warning should come up
    WARN_RATE = 0.125
    WARN_X0 = WARN_RATE*SIZE_X
    WARN_X1 = (1-WARN_RATE)*SIZE_X
    WARN_Y0 = WARN_RATE*SIZE_Y
    WARN_Y1 = (1-WARN_RATE)*SIZE_Y
    # Start margin (so the sub won't hit the wall at start)
    MARGIN_RATE = 0.2
    MARGIN_X = MARGIN_RATE*SIZE_X
    MARGIN_Y = MARGIN_RATE*SIZE_Y

    def is_valid_position(self, x, y):
        return True if 0 < x < Area.SIZE_X and 0 < y < Area.SIZE_Y else False

    def is_warning_position(self, x, y):
        return not (x > Area.WARN_X0 and x < Area.WARN_X1 and y > Area.WARN_Y0 and y < Area.WARN_Y1)

    def __init__(self):
        self.vessels = []

    def diagonal_length(self):
        return np.sqrt(np.power(self.SIZE_X,2) + np.power(self.SIZE_Y,2))

