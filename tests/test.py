import unittest as t
from core import Coord

class TestCoord(t.TestCase):
    def test_init(self):
        c = Coord(1, 1)
        self.assertEqual(c.get(), (1, 1))

    def test_add(self):
        c1 = Coord(1, 2)
        c2 = Coord(3, 4)
        self.assertEqual((c1 + c2).get(), (4, 6))

    def test_sub(self):
        c1 = Coord(1, 2)
        c2 = Coord(3, 5)
        self.assertEqual((c2 - c1).get(), (2, 3))
        self.assertEqual((c2 - c2).get(), (0, 0))

    def test_str(self):
        c = Coord(1, 2)
        self.assertEqual(str(c), '(1, 2)')
