import Tkinter
import random

import Numpy as np

from server.Area import Area


class Weapon:

    TARGETING_WIDTH = np.pi / 16

    def __init__(self, area, source):
        self.area = area
        self.source = source

    def fire(self):
        for target in self.area.vessels:
            dx = target.x - self.source.x
            dy = target.y - self.source.y
            angle = np.arctan(dy/dx)
            if angle - self.source.angle < Weapon.TARGETING_WIDTH:
                distance = np.sqrt(dx^2 + dy^2)
                probability = (1-distance/((Area.SIZE_X+Area.SIZE_Y)/2))
                if random.randrange(0,probability) > 0:
                    return True
