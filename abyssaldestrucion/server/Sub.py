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
    ANGLE_CHANGE_WIDTH = np.pi / 256
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
        self.__change_angle()
        x = self.x + cos(self.angle) * self.STEP_SIZE
        y = self.y + sin(self.angle) * self.STEP_SIZE
        return self.__change_position(x, y)

    def __change_angle(self):
        self.angle += self.angle_change
        if self.angle >= np.pi*2:
            self.angle -= np.pi*2
        if self.angle <= -np.pi*2:
            self.angle += np.pi*2

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
        dx = min(abs(self.x - self.area.SIZE_X), self.x)
        dy = min(abs(self.y - self.area.SIZE_Y), self.y)
        rdx = dx/(Area.WARN_RATE*Area.SIZE_X)
        rdy = dy/(Area.WARN_RATE*Area.SIZE_Y)
        return min(abs(1-rdx),abs(1-rdy))

    def rel_distance_edge(self):
        # TODO: Not scalling correctly
        return max(int(self.__distance_edge()*self.WARNING_POSITIONS),self.WARNING_POSITIONS)
