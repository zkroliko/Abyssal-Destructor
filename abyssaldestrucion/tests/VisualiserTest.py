import unittest

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
        v.start()
        for i in range(0, 100):
            sub1.move()
            v.draw()
        v.master.mainloop()


if __name__ == '__main__':
    unittest.main()
