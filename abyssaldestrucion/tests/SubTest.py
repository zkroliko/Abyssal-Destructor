import unittest

from server.Area import Area
from server.Sub import Sub


class TestSubClass(unittest.TestCase):
    def test_range(self):
        for i in range(0, 100):
            sub = Sub()
            self.assertTrue(0 < sub.x < Area.SIZE_X)
            self.assertTrue(0 < sub.y < Area.SIZE_Y)


if __name__ == '__main__':
    unittest.main()
