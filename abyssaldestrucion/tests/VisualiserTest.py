import unittest

from server.Area import Area
from server.Sub import Sub
from server.Visualiser import Visualiser


class TestSubClass(unittest.TestCase):
    def test_init(self):
        a = Area()
        a.vessels.append(Sub(a))
        a.vessels.append(Sub(a))
        a.vessels.append(Sub(a))

        v = Visualiser(a)
        v.start()
        v.draw()
        v.master.mainloop()



if __name__ == '__main__':
    unittest.main()
