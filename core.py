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
            # TODO: improve
            raise BaseException('unreachable')
