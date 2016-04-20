import random

from server.Area import Area


class Sub:
    STEP_SIZE = 20.0

    def __init__(self, area, x=None, y=None):
        if x is None or y is None:
            self.area = area
            self.x = random.uniform(0, Area.SIZE_X)
            self.y = random.uniform(0, Area.SIZE_Y)

    def change_position(self, x, y):
        if self.area.is_valid_position(x, y):
            self.x = x
            self.y = y
        else:
            # raise some exception or do nothing
        

    def change_orientation(self, value):
        pass


