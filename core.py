import copy
import random


class UnreachableError(BaseException):
    def __str__(self):
        return 'unreachable'


class Coord:
    '''
    Coord class is 2 dimention vector for expressing coordinates.
    '''

    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def __add__(self, other):
        return Coord(self.__x + other.__x, self.__y + other.__y)

    def __sub__(self, other):
        return Coord(self.__x - other.__x, self.__y - other.__y)

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'({self.__x}, {self.__y})'

    def set(self, newCoord):
        self.__x, self.__y = newCoord.__x, newCoord.__y

    def get(self):
        return (self.__x, self.__y)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value


class Stone:
    '''
    Stone class holds constants to specify cell states, and some operatons to
    the constants such as a method to get representative characters of cell
    states.
    '''

    (
        White,
        Black,
        Unset,
        Surrounding,
        OutOfRange
    ) = list(range(5))
    _AlternateChar = ('o', 'x', '.', '*', ' ')
    _MapCharToStone = \
        dict(zip(_AlternateChar, range(len(_AlternateChar))))

    class InvalidStoneError(BaseException):
        def __str__(self):
            return 'Stone must be white or black'

    @staticmethod
    def to_char(stone):
        return Stone._AlternateChar[stone]

    @staticmethod
    def char_to_stone(char):
        return Stone._MapCharToStone[char]

    @staticmethod
    def get_rival_stone_color(stone):
        if stone == Stone.White:
            return Stone.Black
        elif stone == Stone.Black:
            return Stone.White
        else:
            raise Stone.InvalidStoneError()


class Board:
    '''
    Board class provides primitive operations for 8x8 matrix.
    '''

    Size = 8

    def __init__(self):
        self.init_state()

    def init_state(self):
        self.__board = [[Stone.Unset for _ in range(8)] for _ in range(8)]
        self.__stones_count = [0, 0]

    def is_valid_coord(self, coord):
        (x, y) = coord.get()
        return 0 <= x <= (Board.Size - 1) and 0 <= y <= (Board.Size - 1)

    def set_stone(self, coord, stone):
        '''
        set_stone(coord, stone)
            Set cell in the position 'coord' to 'stone'. Return True if
            success.
        '''
        if not self.is_valid_coord(coord):
            return False
        (x, y) = coord.get()
        origin = self.get_stone(coord)
        self.__board[y][x] = stone

        # Update counts of stones
        for color in [Stone.White, Stone.Black]:
            if origin == color:
                self.__stones_count[color] -= 1
            if stone == color:
                self.__stones_count[color] += 1

        return True

    def get_stone(self, coord):
        if not self.is_valid_coord(coord):
            return Stone.OutOfRange
        (x, y) = coord.get()
        return self.__board[y][x]

    def get_white_stones_count(self):
        return self.__stones_count[Stone.White]

    def get_black_stones_count(self):
        return self.__stones_count[Stone.Black]

    def get_stones_counts(self):
        return copy.copy(self.__stones_count)

    # Stringify the board, convenient for debugging.
    def __str__(self):
        visualized = ''
        for stones in self.__board:
            for stone in stones:
                visualized += Stone.to_char(stone)
            visualized += "\n"
        return visualized[:-1]  # Remove the last "\n"

    def print_board(self):
        '''
        print_board():
            Print the board, in format easy to see for humans.
        '''
        print("o ... White stone")
        print("x ... Black stone")
        print("  0 1 2 3 4 5 6 7")
        sep = " +-+-+-+-+-+-+-+-+"
        for linenr in range(len(self.__board)):
            print(sep)
            line = str(linenr)
            for stone in self.__board[linenr]:
                c = ' '
                if stone == Stone.White:
                    c = 'o'
                elif stone == Stone.Black:
                    c = 'x'
                line += '|' + c
            line += '|'
            print(line)
        print(sep)

    # Set entire board matrix. Mainly for debugging.
    def set_entire(self, board):
        self.__stones_count = [0, 0]
        self.__board = copy.deepcopy(board)
        for line in self.__board:
            for cell in line:
                for color in [Stone.White, Stone.Black]:
                    if cell == color:
                        self.__stones_count[color] += 1

    def get_entire(self):
        return copy.deepcopy(self.__board)


class CPU:
    class Score:
        Corner = 200
        CornerSide = 100
        AroundCorner = -100
        Normal = 0
        Default = -100

    '''
    get_put_coord(reversi, color)
        Return a coord to put stone. This function assumes that `color` player
        can put stone at least one place.
    '''
    @staticmethod
    def get_put_coord(reversi, color):
        maxScore = CPU.Score.Default
        coords = []
        for c in reversi.get_puttable_coords(color):
            score = CPU.get_score_of_coord(reversi, c, color)
            if score > maxScore:
                maxScore = score
                coords = [c]
            elif score == maxScore:
                coords.append(c)
        return coords[random.randrange(len(coords))]    # Select one randomly

    @staticmethod
    def get_score_of_coord(reversi, coord, color):
        # The score is {Base score} + {Additional score}.
        # The base score is calculated by the position on the boord.
        # The additional score is the count of how many stones are reversed.
        return CPU.get_base_score_of_coord(reversi, coord, color) + \
            len(reversi.get_all_sandwiched_stones_coords(coord, color))

    '''
    get_base_score_of_coord(reversi, coord, color)
        Calculate the base score of `coord` position by checking the position
        on the board.
    '''
    @staticmethod
    def get_base_score_of_coord(reversi, coord, color):
        (x, y) = coord.get()
        if CPU.is_corner(coord):
            return CPU.Score.Corner

        # Check for * positions
        #
        #   +---
        #   |o*
        #
        #   +-----
        #   |ooo*
        #
        #   +-----
        #   |oxx*
        #
        directions = []
        if x == 0 or x == Board.Size - 1:
            directions = [Coord(0, -1), Coord(0, 1)]
        elif y == 0 or y == Board.Size - 1:
            directions = [Coord(-1, 0), Coord(1, 0)]

        if len(directions) != 0:
            rival_color = Stone.get_rival_stone_color(color)
            board = reversi.get_board()
            for d in directions:
                c = coord + d
                while board.get_stone(c) == rival_color:
                    c += d
                while board.get_stone(c) == color:
                    if CPU.is_corner(c):
                        return CPU.Score.CornerSide
                    c += d

        # Check for * positions
        #  +--- ... ---+
        #  | *       * |
        #  |**       **|
        #  .           .
        #  |**       **|
        #  | *       * |
        #  +--- ... ---+
        if (x <= 1 or x >= Board.Size - 2) and (y <= 1 or y >= Board.Size - 2):
            return CPU.Score.AroundCorner

        return CPU.Score.Normal

    @staticmethod
    def is_corner(coord):
        (x, y) = coord.get()
        if (x == 0 or x == Board.Size - 1) and (y == 0 or y == Board.Size - 1):
            return True
        return False


class Reversi:
    '''
    Reversi class provides reversi game related operations
    '''
    EightDirections = [
        Coord(1, 0),
        Coord(1, 1),
        Coord(0, 1),
        Coord(-1, 1),
        Coord(-1, 0),
        Coord(-1, -1),
        Coord(0, -1),
        Coord(1, -1),
    ]

    class PlayMode:
        VsPlayer = 0
        VsCPU = 1

    def __init__(self):
        self.__board = Board()
        self.__play_mode = Reversi.PlayMode.VsPlayer
        self.init_state()

    def init_state(self):
        self.__player_color = Stone.White
        self.__board.init_state()

        # Initialize board like this:
        #   o ... White stone
        #   x ... Black stone
        #   * ... Cells surrounding stones
        #      0 1 2 3 4 5 6 7  --> x
        #     +-+-+-+-+-+-+-+-+
        #    0| | | | | | | | |
        #     +-+-+-+-+-+-+-+-+
        #    1| | | | | | | | |
        #     +-+-+-+-+-+-+-+-+
        #    2| | |*|*|*|*| | |
        #     +-+-+-+-+-+-+-+-+
        #    3| | |*|o|x|*| | |
        #     +-+-+-+-+-+-+-+-+
        #    4| | |*|x|o|*| | |
        #     +-+-+-+-+-+-+-+-+
        #    5| | |*|*|*|*| | |
        #     +-+-+-+-+-+-+-+-+
        #    6| | | | | | | | |
        #     +-+-+-+-+-+-+-+-+
        #    7| | | | | | | | |
        #     +-+-+-+-+-+-+-+-+
        #    |
        #    |
        #  y v
        self.__board.set_stone(Coord(3, 3), Stone.White)
        self.__board.set_stone(Coord(4, 4), Stone.White)
        self.__board.set_stone(Coord(3, 4), Stone.Black)
        self.__board.set_stone(Coord(4, 3), Stone.Black)

        surrounding_cells = [
            Coord(2, 2),
            Coord(2, 3),
            Coord(2, 4),
            Coord(2, 5),
            Coord(3, 2),
            Coord(3, 5),
            Coord(4, 2),
            Coord(4, 5),
            Coord(5, 2),
            Coord(5, 3),
            Coord(5, 4),
            Coord(5, 5),
        ]
        for c in surrounding_cells:
            self.__board.set_stone(c, Stone.Surrounding)

    def get_sandwiched_stones_coords(self, coord, direction, color):
        '''
        get_sandwiched_stones_coords(coord, direction, color):
            Return coords of stones sandwiched by 'color' stones in direction
            of 'direction' from position 'coord'
            The position 'coord' must points a valid position.
        '''
        rival_color = Stone.get_rival_stone_color(color)
        p = coord
        coords = []
        while True:
            p += direction
            s = self.__board.get_stone(p)
            if s == color:
                return coords
            elif s == rival_color:
                coords.append(p)
            else:
                return []

    def get_all_sandwiched_stones_coords(self, coord, color):
        coords = []
        for d in Reversi.EightDirections:
            coords.extend(self.get_sandwiched_stones_coords(coord, d, color))
        return coords

    def can_put_here(self, coord, color):
        '''
        can_put_here(coord, color):
            Return TRUE if stone of 'color' can put on 'coord'
        '''
        if self.__board.get_stone(coord) != Stone.Surrounding:
            return False
        for d in Reversi.EightDirections:
            if len(self.get_sandwiched_stones_coords(coord, d, color)) > 0:
                return True
        return False

    def put_stone_color(self, coord, color):
        '''
        put_stone_color(coord, color):
            Put stone of 'color' to the position 'coord', and reverse the
            stones sandwiched by the new stone and some existing stone whose
            color is 'color' too.

            Also checks how many white/black stones on the board, and checks if
            either player wins.
        '''
        if not self.can_put_here(coord, color):
            # Cannot put here
            # TODO: Notify
            return

        # Put new stone
        self.__board.set_stone(coord, color)
        for d in Reversi.EightDirections:
            if self.__board.get_stone(coord + d) == Stone.Unset:
                self.__board.set_stone(coord + d, Stone.Surrounding)

        # Reverse sandwiched stones
        for p in self.get_all_sandwiched_stones_coords(coord, color):
            self.__board.set_stone(p, color)

        # Check if either player wins
        # TODO: Notify
        w = self.__board.get_white_stones_count()
        b = self.__board.get_black_stones_count()
        if w <= 0:
            pass
        elif b <= 0:
            pass
        elif (w + b) >= Board.Size ** 2:
            pass

    def put_stone(self, coord):
        self.put_stone_color(coord, self.__player_color)

    def proceed_to_next(self):
        '''
        proceed_to_next():
            Go on to the next player's turn.

            If the next player can put nowhere, notify players that the next
            player need pass, and continue the current player's turn.

            Also, if the rival player is CPU, do the CPU's action, and return
            back to the current player's turn.
        '''

        next_player = Stone.get_rival_stone_color(self.__player_color)
        if self.need_pass(next_player):
            # TODO: Notify
            return

        if self.get_play_mode() == Reversi.PlayMode.VsCPU:
            while True:
                self.put_stone_color(
                        CPU.get_put_coord(self, next_player), next_player)
                if self.need_pass(self.__player_color):
                    # TODO: Notify
                    pass
                else:
                    break

        self.__player_color = next_player

    def need_pass(self, color):
        for x in range(Board.Size):
            for y in range(Board.Size):
                if self.can_put_here(Coord(x, y), color):
                    return False
        return True

    def get_puttable_coords(self, color=None):
        if color is None:
            color = self.get_player_color()
        puttable_coords = []
        for y in range(Board.Size):
            for x in range(Board.Size):
                c = Coord(x, y)
                if self.can_put_here(c, color):
                    puttable_coords.append(c)
        return puttable_coords

    def set_play_mode(self, mode):
        self.__play_mode = mode

    def get_play_mode(self):
        return self.__play_mode

    def get_player_color(self):
        return self.__player_color

    def get_board(self):
        return self.__board
