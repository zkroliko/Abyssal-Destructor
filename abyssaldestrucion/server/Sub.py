import random

import numpy as np
from numpy.core.umath import cos, sin

from server.Area import Area


class Sub:
    # How far the sub moves in one iteration
    STEP_SIZE = 2.0

    # For validating input
    ORIENTATION_MIN = 0
    ORIENTATION_MAX = 31
    # How the sub changes direction
    ANGLE_CHANGE_WIDTH = np.pi / 8
    ORIENTATION_TO_ANGLE = ANGLE_CHANGE_WIDTH / (ORIENTATION_MAX - ORIENTATION_MIN)


    def __init__(self, area, x=None, y=None):
        if x is None or y is None:
            self.x = random.uniform(Area.MARGIN_X, Area.SIZE_X - Area.MARGIN_X)
            self.y = random.uniform(Area.MARGIN_Y, Area.SIZE_Y - Area.MARGIN_Y)
        else:
            self.x = x
            self.y = y
        self.area = area
        self.angle = 0
        self.angle_change = 0

    def change_position(self, x, y):
        if self.area.is_valid_position(x, y):
            self.x = x
            self.y = y
        else:
            pass
            # raise some exception or do nothing
        
    def change_orientation(self, value):
        val = min(self.ORIENTATION_MAX, max(self.ORIENTATION_MIN, value))
        self.angle_change = self.__map_angle(val)

    def move(self):
        x = self.x + cos(self.angle) * self.STEP_SIZE
        y = self.y + sin(self.angle) * self.STEP_SIZE
        self.change_position(x,y)

    def __map_angle(self, angle):
        return self.angle_change * self.ORIENTATION_TO_ANGLE

