import unittest as t
import view


class TestCanvasCoord(t.TestCase):
    def test_x(self):
        c1 = view.CanvasCoord(1, 3)
        c2 = view.CanvasCoord(0, 3)
        self.assertEqual(c1.x, 1)

        c2.x = 3
        self.assertEqual(c2.x, 3)

    def test_y(self):
        c1 = view.CanvasCoord(1, 1)
        c2 = view.CanvasCoord(0, 3)
        self.assertEqual(c1.y, 1)

        c2.y = 4
        self.assertEqual(c2.y, 4)
