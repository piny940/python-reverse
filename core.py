import copy


class UnreachableError(BaseException):
    def __str__(self):
        return 'unreachable'


class Coord:
    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def __add__(self, other):
        return Coord(self.__x + other.__x, self.__y + other.__y)

    def __sub__(self, other):
        return Coord(self.__x - other.__x, self.__y - other.__y)

    def __str__(self):
        return f'({self.__x}, {self.__y})'

    def set(self, newCoord):
        self.__x, self.__y = newCoord.__x, newCoord.__y

    def get(self):
        return (self.__x, self.__y)


class Stone:
    # Constants to specify cell states.
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
    Size = 8

    def __init__(self):
        self.init_state()

    def init_state(self):
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
        self.__board = [[Stone.Unset for _ in range(8)] for _ in range(8)]
        self.__stones_count = [0, 0]

        self.set_stone(Coord(3, 3), Stone.White)
        self.set_stone(Coord(4, 4), Stone.White)
        self.set_stone(Coord(3, 4), Stone.Black)
        self.set_stone(Coord(4, 3), Stone.Black)

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
            self.set_stone(c, Stone.Surrounding)

    def is_valid_coord(self, coord):
        (x, y) = coord.get()
        return 0 <= x <= (Board.Size - 1) and 0 <= y <= (Board.Size - 1)

    # Set stone of position 'coord' to 'stone'. Return True if success.
    def set_stone(self, coord, stone):
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

    # Stringify the board, convenient for debugging.
    def __str__(self):
        visualized = ''
        for stones in self.__board:
            for stone in stones:
                visualized += Stone.to_char(stone)
            visualized += "\n"
        return visualized[:-1]  # Remove the last "\n"

    # Print the board, in format easy to see for humans.
    def print_board(self):
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


class Reversi:
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

    def __init__(self):
        self.__player_color = Stone.White
        self.__board = Board()

    # Return how many stones are sandwiched by 'color' stones in direction of
    # 'direction' from position 'coord'
    def get_sandwiched_stones_count(self, coord, direction, color):
        rival_color = Stone.get_rival_stone_color(color)
        p = coord + direction
        if self.__board.get_stone(p) != rival_color:
            return 0

        count = 1
        while True:
            p += direction
            s = self.__board.get_stone(p)
            if s == color:
                return count
            elif s == rival_color:
                count += 1
            else:
                return 0

    # Return TRUE if stone of 'color' can put on 'coord'
    def can_put_here(self, coord, color):
        if self.__board.get_stone(coord) != Stone.Surrounding:
            return False
        for d in Reversi.EightDirections:
            if self.get_sandwiched_stones_count(coord, d, color) > 0:
                return True
        return False

    def put_stone_color(self, coord, color):
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
        for d in Reversi.EightDirections:
            count = self.get_sandwiched_stones_count(coord, d, color)
            if count == 0:
                continue

            p = coord
            for _ in range(count):
                p += d
                self.__board.set_stone(p, color)

        # Check if someone wins
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

    def next_turn(self):
        next_player = Stone.get_rival_stone_color(self.__player_color)

        for x in range(Board.Size):
            for y in range(Board.Size):
                if self.can_put_here(Coord(x, y), next_player):
                    self.__player_color = next_player
                    return
        # If the next player can put stone nowhere, reaches here.
        # TODO: Notify

    def get_player_color(self):
        return self.__player_color

    def get_board(self):
        return self.__board
