import unittest

import numpy

from server.Area import Area
from server.Sub import Sub


class TestSubClass(unittest.TestCase):
    def test_range(self):
        for i in range(0, 100):
            sub = Sub()
            self.assertTrue(0 < sub.x < Area.SIZE_X)
            self.assertTrue(0 < sub.y < Area.SIZE_Y)

    def test_move(self):
        expected = {
            0.0: (Sub.STEP_SIZE, 0),
            numpy.pi / 2: (0, Sub.STEP_SIZE),
            numpy.pi: (-Sub.STEP_SIZE, 0),
            numpy.pi * 3 / 2: (0, -Sub.STEP_SIZE),
        }

        for a, (x, y) in expected.iteritems():
            sub = Sub(500, 500)
            sub.angle = a
            sub.move()
            self.assertEqual(sub.x, 500 + x)
            self.assertEqual(sub.y, 500 + y)



if __name__ == '__main__':
    unittest.main()
