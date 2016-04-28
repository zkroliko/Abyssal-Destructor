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
                angle = self.__get_angle(target)
                angle_difference = abs(abs(angle) - abs(self.source.angle))
                print "----Data"
                print "Mine %s" % self.source.angle
                print "Target %s" % angle
                print "-------------------"

                print "Have %s" % angle_difference
                print "Need %s" % self.TARGETING_WIDTH
                if angle_difference < Weapon.TARGETING_WIDTH:
                    dx = target.x - self.source.x
                    dy = target.y - self.source.y
                    distance = np.sqrt(np.power(dx,2) + np.power(dy,2))
                    probability = (1-distance/((Area.SIZE_X+Area.SIZE_Y)/2))
                    if random.uniform(0, probability) > 0:
                        hit.append(target)
        return hit

    def __get_angle(self, target):
        dx = target.x - self.source.x
        dy = target.y - self.source.y
        if target.x > self.source.x and target.y > self.source.y:
            angle = np.arctan(dy/dx)
            return angle
        elif target.x < self.source.x and target.y > self.source.y:
            angle = np.arctan(dx/dy)
            return angle + np.pi/2
        elif target.x < self.source.x and target.y < self.source.y:
            angle = np.arctan(dx/dy)
            return angle + np.pi
        else:
            angle = np.arctan(dy/dx)
            return angle + np.pi*3/2

