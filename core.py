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
    White = 0
    Black = 1
    Unset = 2
    Surrounding = 3
    OutOfRange = 4

    class InvalidStoneError(BaseException):
        def __str__(self):
            return 'Stone must be white or black'

    @staticmethod
    def to_string(stone):
        if stone == Stone.White:
            return 'o'
        elif stone == Stone.Black:
            return 'x'
        elif stone == Stone.Unset:
            return '.'
        elif stone == Stone.Surrounding:
            return '*'
        elif stone == Stone.OutOfRange:
            return ' '
        else:
            raise UnreachableError()

    @staticmethod
    def rival_stone_color(stone):
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
        #      0 1 2 3 4 5 6 7
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
        self.__board[x][y] = stone

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
        return self.__board[x][y]

    def get_white_stones_count(self):
        return self.__stones_count[Stone.White]

    def get_black_stones_count(self):
        return self.__stones_count[Stone.Black]

    def __str__(self):
        visualized = ''
        for stones in self.__board:
            for stone in stones:
                visualized += Stone.to_string(stone)
            visualized += "\n"
        return visualized[:-1]  # Remove the last "\n"

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
