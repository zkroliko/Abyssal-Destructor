import random

from server.Area import Area


class Sub:
    STEP_SIZE = 20.0

    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = random.uniform(0, Area.SIZE_X)
            self.y = random.uniform(0, Area.SIZE_Y)

    def change_orientation(self, value):
        pass


