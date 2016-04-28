import random

import numpy as np

from server.Area import Area


class Weapon:

    TARGETING_WIDTH = np.pi / 16

    def __init__(self, source):
        self.source = source
        self.area = source.area

    def hit_by_firing(self):
        hit = []
        for target in self.area.vessels:
            if target is not self.source:
                dx = target.x - self.source.x
                dy = target.y - self.source.y
                angle = np.arctan(dy/dx)
                if angle - self.source.angle < Weapon.TARGETING_WIDTH:
                    distance = np.sqrt(np.power(dx,2) + np.power(dy,2))
                    probability = (1-distance/((Area.SIZE_X+Area.SIZE_Y)/2))
                    if random.uniform(0, probability) > 0:
                        hit.append(target)
        return hit
