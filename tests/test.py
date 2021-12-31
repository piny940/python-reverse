import unittest as t
import textwrap
import core
import view


def trim_for_board(s):
    return textwrap.dedent(s).strip()


def board_string_to_matrix(s):
    matrix = []
    lines = trim_for_board(s).split("\n")
    if len(lines) != core.Board.Size:
        raise BaseException('Invalid size of lines')
    for line in lines:
        if len(line) != core.Board.Size:
            raise BaseException('Invalid size of columns')
        matrix_line = []
        for c in line:
            matrix_line.append(core.Stone.char_to_stone(c))
        matrix.append(matrix_line)
    return matrix


class TestUtilityFunctions(t.TestCase):
    def test_board_string_to_matrix(self):
        board_string = trim_for_board('''
            ........
            ........
            ..****..
            ..*oo*..
            ..*xo*..
            ..****..
            ........
            ........
        ''')

        w = core.Stone.White
        b = core.Stone.Black
        u = core.Stone.Unset
        s = core.Stone.Surrounding
        board_matrix = [
                [u, u, u, u, u, u, u, u],
                [u, u, u, u, u, u, u, u],
                [u, u, s, s, s, s, u, u],
                [u, u, s, w, w, s, u, u],
                [u, u, s, b, w, s, u, u],
                [u, u, s, s, s, s, u, u],
                [u, u, u, u, u, u, u, u],
                [u, u, u, u, u, u, u, u],
        ]
        self.assertEqual(
                board_string_to_matrix(board_string),
                board_matrix)


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

    def test_eq(self):
        base = core.Coord(0, 0)
        self.assertTrue(base == core.Coord(0, 0))
        self.assertFalse(base == core.Coord(1, 0))
        self.assertFalse(base == core.Coord(0, 1))
        self.assertFalse(base == core.Coord(1, 1))

    def test_ne(self):
        base = core.Coord(0, 0)
        self.assertTrue(base != core.Coord(1, 0))
        self.assertTrue(base != core.Coord(0, 1))
        self.assertTrue(base != core.Coord(1, 1))
        self.assertFalse(base != core.Coord(0, 0))

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

class TestStone(t.TestCase):
    def test_to_char(self):
        self.assertEqual(core.Stone.to_char(core.Stone.White), 'o')
        self.assertEqual(core.Stone.to_char(core.Stone.Black), 'x')
        self.assertEqual(core.Stone.to_char(core.Stone.Unset), '.')
        self.assertEqual(core.Stone.to_char(core.Stone.Surrounding), '*')
        self.assertEqual(core.Stone.to_char(core.Stone.OutOfRange), ' ')

        with self.assertRaises(IndexError):
            core.Stone.to_char(100)

    def test_rival_stone_color(self):
        self.assertEqual(
                core.Stone.get_rival_stone_color(core.Stone.White),
                core.Stone.Black)
        self.assertEqual(
                core.Stone.get_rival_stone_color(core.Stone.Black),
                core.Stone.White)
        for s in [
                core.Stone.Unset,
                core.Stone.Surrounding,
                core.Stone.OutOfRange]:
            with self.assertRaises(core.Stone.InvalidStoneError):
                core.Stone.get_rival_stone_color(s)


class TestBoard(t.TestCase):
    def test_str(self):
        c = core.Board()
        expected = trim_for_board('''
            ........
            ........
            ........
            ........
            ........
            ........
            ........
            ........
        ''')
        self.assertEqual(str(c), expected)

    def test_is_valid_coord(self):
        c = core.Board()
        self.assertTrue(c.is_valid_coord(core.Coord(0, 0)))
        self.assertTrue(c.is_valid_coord(core.Coord(7, 1)))
        self.assertTrue(c.is_valid_coord(core.Coord(1, 7)))
        self.assertFalse(c.is_valid_coord(core.Coord(-1, 1)))
        self.assertFalse(c.is_valid_coord(core.Coord(8, 1)))
        self.assertFalse(c.is_valid_coord(core.Coord(1, -1)))
        self.assertFalse(c.is_valid_coord(core.Coord(1, 8)))

    def test_set_entire(self):
        board_string = '''
            ******..
            *o**x*..
            ******..
            ..*ox*..
            ..*xo**.
            ..***o**
            ....*ooo
            ....****
        '''
        c = core.Board()
        c.set_entire(board_string_to_matrix(board_string))
        self.assertEqual(str(c), trim_for_board(board_string))
        self.assertEqual(c.get_white_stones_count(), 7)
        self.assertEqual(c.get_black_stones_count(), 3)

    def test_get_stone(self):
        c = core.Board()
        c.set_entire(board_string_to_matrix('''
            ........
            ........
            ..****..
            ..*ox*..
            ..*xo*..
            ..****..
            ........
            ........
        '''))
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
        c.set_entire(board_string_to_matrix('''
            ........
            ........
            ..****..
            ..*ox*..
            ..*xo*..
            ..****..
            ........
            ........
        '''))
        p = core.Coord(0, 0)
        c.set_stone(p, core.Stone.White)
        self.assertEqual(c.get_stone(p), core.Stone.White)

        c1, c2 = core.Board(), core.Board()
        r = c1.set_stone(core.Coord(-1, -1), core.Stone.White)
        self.assertFalse(r)
        self.assertEqual(str(c1), str(c2))

    def test_stones_count(self):
        c = core.Board()
        self.assertEqual(c.get_white_stones_count(), 0)
        self.assertEqual(c.get_black_stones_count(), 0)

        c.set_entire(board_string_to_matrix('''
            ........
            ........
            ..****..
            ..*ox*..
            ..*xo*..
            ..****..
            ........
            ........
        '''))
        self.assertEqual(c.get_white_stones_count(), 2)
        self.assertEqual(c.get_black_stones_count(), 2)

        c.set_stone(core.Coord(0, 0), core.Stone.White)
        self.assertEqual(c.get_white_stones_count(), 3)
        self.assertEqual(c.get_black_stones_count(), 2)

        c.set_stone(core.Coord(0, 0), core.Stone.Black)
        self.assertEqual(c.get_white_stones_count(), 2)
        self.assertEqual(c.get_black_stones_count(), 3)

    def test_init_state(self):
        initial_state = trim_for_board('''
            ........
            ........
            ........
            ........
            ........
            ........
            ........
            ........
        ''')
        c = core.Board()
        c.set_stone(core.Coord(0, 0), core.Stone.White)
        c.set_stone(core.Coord(1, 1), core.Stone.Black)
        self.assertNotEqual(str(c), initial_state)
        c.init_state()
        self.assertEqual(str(c), initial_state)


# TODO: Add tests for unputtable place
class TestReversi(t.TestCase):
    def test_can_put_here(self):
        r = core.Reversi()
        self.assertTrue(r.can_put_here(core.Coord(4, 2), core.Stone.White))
        self.assertTrue(r.can_put_here(core.Coord(2, 3), core.Stone.Black))
        self.assertFalse(r.can_put_here(core.Coord(4, 2), core.Stone.Black))
        self.assertFalse(r.can_put_here(core.Coord(2, 3), core.Stone.White))
        self.assertFalse(r.can_put_here(core.Coord(3, 3), core.Stone.White))
        self.assertFalse(r.can_put_here(core.Coord(1, 1), core.Stone.White))
        self.assertFalse(r.can_put_here(core.Coord(8, 8), core.Stone.White))

    def test_get_sandwiched_stones_coords(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            **xxxxxx
            *xx*****
            *o*x**..
            *o**x**.
            *****o*.
            ....***.
            ........
            ........
        '''))

        def get_coords(direction):
            return r.get_sandwiched_stones_coords(
                core.Coord(1, 0), direction, core.Stone.White)

        self.assertEqual(get_coords(core.Coord(-1, 0)), [])
        self.assertEqual(get_coords(core.Coord(0, -1)), [])
        self.assertEqual(get_coords(core.Coord(1, 0)), [])
        self.assertEqual(get_coords(core.Coord(1, 1)), [
                core.Coord(2, 1),
                core.Coord(3, 2),
                core.Coord(4, 3)
            ])
        self.assertEqual(get_coords(core.Coord(0, 1)), [
                core.Coord(1, 1),
            ])

    def test_get_all_sandwiched_stones_coords_1(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            **xxxxxx
            *xx*****
            *o*x**..
            *o**x**.
            *****o*.
            ....***.
            ........
            ........
        '''))
        self.assertEqual(
                r.get_all_sandwiched_stones_coords(
                    core.Coord(1, 0),
                    core.Stone.White),
                [
                    core.Coord(2, 1),
                    core.Coord(3, 2),
                    core.Coord(4, 3),
                    core.Coord(1, 1)
                ])

    def test_get_all_sandwiched_stones_coords_2(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            ........
            ........
            ........
            ...***..
            ...*x*..
            ...***..
            ........
            ........
        '''))
        self.assertEqual(
                r.get_all_sandwiched_stones_coords(
                    core.Coord(4, 3),
                    core.Stone.White),
                [])

    def test_put_stone_color_1(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            ........
            ***.....
            *x*.....
            *x*.....
            *o*.....
            ***.....
            ........
            ........
        '''))
        r.put_stone_color(core.Coord(1, 1), core.Stone.White)
        self.assertEqual(str(r.get_board()), trim_for_board('''
            ***.....
            *o*.....
            *o*.....
            *o*.....
            *o*.....
            ***.....
            ........
            ........
        '''))
        self.assertEqual(r.get_board().get_white_stones_count(), 4)
        self.assertEqual(r.get_board().get_black_stones_count(), 0)

    def test_put_stone_color_2(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            ........
            ****....
            *xx**...
            *x*x**..
            *o**x**.
            *x***o*.
            *o*.***.
            ***.....
        '''))
        r.put_stone_color(core.Coord(1, 1), core.Stone.White)
        self.assertEqual(str(r.get_board()), trim_for_board('''
            ***.....
            *o**....
            *oo**...
            *o*o**..
            *o**o**.
            *x***o*.
            *o*.***.
            ***.....
        '''))
        self.assertEqual(r.get_board().get_white_stones_count(), 9)
        self.assertEqual(r.get_board().get_black_stones_count(), 1)

    def test_put_stone_color_3(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            .*******
            **xxxxxx
            *xx*****
            *x*x**..
            *o**x**.
            *****o*.
            ....***.
            ........
        '''))
        r.put_stone_color(core.Coord(1, 1), core.Stone.White)
        self.assertEqual(str(r.get_board()), trim_for_board('''
            ********
            *oxxxxxx
            *oo*****
            *o*o**..
            *o**o**.
            *****o*.
            ....***.
            ........
        '''))
        self.assertEqual(r.get_board().get_white_stones_count(), 8)
        self.assertEqual(r.get_board().get_black_stones_count(), 6)

    def test_put_stone_color_4(self):
        r = core.Reversi()
        r.get_board().set_entire(board_string_to_matrix('''
            ........
            .*******
            .*ooooo*
            .*oxxxo*
            .*ox*xo*
            .*oxxxo*
            .*ooooo*
            .*******
        '''))
        r.put_stone_color(core.Coord(4, 4), core.Stone.White)
        self.assertEqual(str(r.get_board()), trim_for_board('''
            ........
            .*******
            .*ooooo*
            .*ooooo*
            .*ooooo*
            .*ooooo*
            .*ooooo*
            .*******
        '''))
        self.assertEqual(r.get_board().get_white_stones_count(), 25)
        self.assertEqual(r.get_board().get_black_stones_count(), 0)

    def test_proceed_to_next_1(self):
        r = core.Reversi()
        self.assertEqual(r.get_player_color(), core.Stone.White)
        r.proceed_to_next()
        self.assertEqual(r.get_player_color(), core.Stone.Black)

    def text_proceed_to_next_2(self):
        r = core.Reversi()
        self.assertEqual(r.get_player_color(), core.Stone.White)
        r.get_board().set_entire(board_string_to_matrix('''
            ........
            ........
            .*****..
            .*xxx*..
            .*xox*..
            .*xxx*..
            .*****..
            ........
        '''))
        r.proceed_to_next()
        # Black has no place to put stone, so they have to pass.
        self.assertEqual(r.get_player_color(), core.Stone.White)
