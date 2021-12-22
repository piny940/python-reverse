import unittest as t
import textwrap
import core


def trim_for_board(s):
    return textwrap.dedent(s).strip()


class TestCoord(t.TestCase):
    def test_init(self):
        c = core.Coord(1, 1)
        self.assertEqual(c.get(), (1, 1))

    def test_add(self):
        c1 = core.Coord(1, 2)
        c2 = core.Coord(3, 4)
        self.assertEqual((c1 + c2).get(), (4, 6))

    def test_sub(self):
        c1 = core.Coord(1, 2)
        c2 = core.Coord(3, 5)
        self.assertEqual((c2 - c1).get(), (2, 3))
        self.assertEqual((c2 - c2).get(), (0, 0))

    def test_str(self):
        c = core.Coord(1, 2)
        self.assertEqual(str(c), '(1, 2)')


class TestBoard(t.TestCase):
    def test_str(self):
        c = core.Board()
        expected = trim_for_board('''
            ........
            ........
            ..****..
            ..*ox*..
            ..*xo*..
            ..****..
            ........
            ........
        ''')
        self.assertEqual(str(c), expected)

    def test_is_valid_coord(self):
        c = core.Board()
        self.assertTrue(c.is_valid_coord(core.Coord(1, 1)))
        self.assertTrue(c.is_valid_coord(core.Coord(7, 1)))
        self.assertTrue(c.is_valid_coord(core.Coord(1, 7)))
        self.assertFalse(c.is_valid_coord(core.Coord(-1, 1)))
        self.assertFalse(c.is_valid_coord(core.Coord(8, 1)))
        self.assertFalse(c.is_valid_coord(core.Coord(1, -1)))
        self.assertFalse(c.is_valid_coord(core.Coord(1, 8)))

    def test_get_stone(self):
        c = core.Board()
        self.assertEqual(c.get_stone(core.Coord(0, 0)), core.Stone.Unset)
        self.assertEqual(c.get_stone(core.Coord(2, 2)), core.Stone.Surrounding)
        self.assertEqual(c.get_stone(core.Coord(3, 3)), core.Stone.White)
        self.assertEqual(c.get_stone(core.Coord(3, 4)), core.Stone.Black)
        self.assertEqual(c.get_stone(core.Coord(-1, 0)), core.Stone.OutOfRange)
        self.assertEqual(c.get_stone(core.Coord(0, -1)), core.Stone.OutOfRange)
        self.assertEqual(c.get_stone(core.Coord(8, 0)), core.Stone.OutOfRange)
        self.assertEqual(c.get_stone(core.Coord(0, 8)), core.Stone.OutOfRange)

    def test_set_stone(self):
        c = core.Board()
        p = core.Coord(0, 0)
        c.set_stone(p, core.Stone.White)
        self.assertEqual(c.get_stone(p), core.Stone.White)

        c1, c2 = core.Board(), core.Board()
        r = c1.set_stone(core.Coord(-1, -1), core.Stone.White)
        self.assertFalse(r)
        self.assertEqual(str(c1), str(c2))

    def test_stones_count(self):
        c = core.Board()
        self.assertEqual(c.get_white_stones_count(), 2)
        self.assertEqual(c.get_black_stones_count(), 2)

        c.set_stone(core.Coord(0, 0), core.Stone.White)
        self.assertEqual(c.get_white_stones_count(), 3)
        self.assertEqual(c.get_black_stones_count(), 2)

        c.set_stone(core.Coord(0, 0), core.Stone.Black)
        self.assertEqual(c.get_white_stones_count(), 2)
        self.assertEqual(c.get_black_stones_count(), 3)
