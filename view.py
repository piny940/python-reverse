import tkinter as tk


class CanvasCoord:
    '''
    CanvasCoord class is 2 dimention vector to express positions in the canvas.
    '''

    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def __add__(self, other):
        return CanvasCoord(self.__x + other.__x, self.__y + other.__y)

    def __sub__(self, other):
        return CanvasCoord(self.__x - other.__x, self.__y - other.__y)

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


class View:
    def __init__(self):
        # Window
        self.__WindowWidth = 500
        self.__WindowHeight = 500

        # Board
        self.__BoardCoord = CanvasCoord(50, 50)
        self.__CellSize = 50

    def create_window(self):
        # ----- Window & Canvas config -----
        window = tk.Tk()
        window.title("Reversi")
        window.geometry(f"{self.__WindowWidth}x{self.__WindowHeight}")

        canvas = tk.Canvas(window, width=self.__WindowWidth,
                            height=self.__WindowHeight)

        canvas.grid(row = 0, column = 0)
    
        # ----- Board -----
        canvas.create_rectangle(
            self.__BoardCoord.x,
            self.__BoardCoord.y,
            self.__BoardCoord.x + self.__CellSize * 8,
            self.__BoardCoord.y + self.__CellSize * 8,
            fill = 'green')

        for i in range(9):
            # Vertical line
            canvas.create_line(
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y,
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y + self.__CellSize * 8,
                fill = 'black')
            
            # Horizontal line
            canvas.create_line(
                self.__BoardCoord.x,
                self.__BoardCoord.y + i * self.__CellSize,
                self.__BoardCoord.x + self.__CellSize * 8,
                self.__BoardCoord.y + i * self.__CellSize,
                fill = 'black')
    
        window.mainloop()
