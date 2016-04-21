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
            sleep(0.05)
            sub1.move()
            sub1.angle += 0.01
            sub2.move()
            sub2.angle += 0.02
            sub3.move()
            sub3.angle += 0.03

            v.step()




if __name__ == '__main__':
    unittest.main()
