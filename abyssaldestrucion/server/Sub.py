import random

import numpy as np
from enum import Enum
from numpy.core.umath import cos, sin

from Area import Area
from server.Weapon import Weapon

class MoveEffect(Enum):
    good = "good"
    warn = "warn"
    bad = "bad"

class Sub:
    # How far the sub moves in one iteration
    STEP_SIZE = 0.5

    # For validating input
    ORIENTATION_MIN = 0
    ORIENTATION_MAX = 63
    # How the sub changes direction
    ANGLE_CHANGE_WIDTH = np.pi / 32
    ORIENTATION_TO_ANGLE = ANGLE_CHANGE_WIDTH / (ORIENTATION_MAX - ORIENTATION_MIN)

    # Warn
    WARNING_POSITIONS = 31

    def __init__(self, area, x=None, y=None, name=None):
        if x is None or y is None:
            self.x = random.uniform(Area.MARGIN_X, Area.SIZE_X - Area.MARGIN_X)
            self.y = random.uniform(Area.MARGIN_Y, Area.SIZE_Y - Area.MARGIN_Y)
        else:
            self.x = x
            self.y = y
        if name is not None:
            self.name = name
        self.area = area
        self.angle = 0
        self.angle_change = 0
        self.weapon = Weapon(self)

    def fire(self):
        return self.weapon.hit_by_firing()

    def __change_position(self, x, y):
        if self.area.is_valid_position(x, y):
            self.x = x
            self.y = y
            if self.area.is_warning_position(x,y):
                return MoveEffect.warn
            else:
                return MoveEffect.good
        else:
            return MoveEffect.bad

    def change_orientation(self, value):
        val = min(self.ORIENTATION_MAX, max(self.ORIENTATION_MIN, value))
        self.angle_change = self.__map_angle(val)

    def move(self):
        self.angle += self.angle_change
        x = self.x + cos(self.angle) * self.STEP_SIZE
        y = self.y + sin(self.angle) * self.STEP_SIZE
        return self.__change_position(x, y)

    def __map_angle(self, angle):
        if angle < Sub.ORIENTATION_MAX / 2:
            return (angle - Sub.ORIENTATION_MAX / 2) * self.ORIENTATION_TO_ANGLE
        else:
            return angle * self.ORIENTATION_TO_ANGLE

    def distance_to(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        return np.sqrt(np.power(dx, 2) + np.power(dy, 2))

    def rel_distance_to(self, target):
        return self.distance_to(target)/self.area.diagonal_length()

    def __distance_edge(self):
        dx = min(self.x - self.area.SIZE_X, self.x)
        dy = min(self.y - self.area.SIZE_Y, self.y)
        rdx = min(self.x - self.area.SIZE_X, self.x)/(Area.WARN_RATE*Area.SIZE_X)
        rdy = min(self.y - self.area.SIZE_Y, self.y)/(Area.WARN_RATE*Area.SIZE_Y)
        print "DATA"
        print rdx
        print rdy
        return min(abs(rdx),abs(rdy))

    def rel_distance_edge(self):
        # TODO: Not scalling correctly
        return int(self.__distance_edge())%self.WARNING_POSITIONS
