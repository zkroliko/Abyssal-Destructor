import random
import unittest
from time import sleep

from server.Area import Area
from server.Sub import Sub
from server.Visualiser import Visualiser


class TestSubClass(unittest.TestCase):
    def test_init(self):
        a = Area()
        sub1 = Sub(a)
        sub2 = Sub(a)
        sub3 = Sub(a)
        a.vessels.append(sub1)
        a.vessels.append(sub2)
        a.vessels.append(sub3)

        v = Visualiser(a)

        for i in range(0, 5000):
            sleep(0.02)
            random.seed(i)
            sub1.change_orientation(random.randrange(0,63))
            sub1.move()
            sub2.change_orientation(random.randrange(0,63))
            sub2.move()
            sub3.change_orientation(random.randrange(0,63))
            sub3.move()

            v.step()




if __name__ == '__main__':
    unittest.main()
