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
    def create_window(self):
        window = tk.Tk()

        window.title("Reversi")
        window.geometry("500x500")

        canvas = tk.Canvas(window, width=500, height=500)
        canvas.grid(row=0, column=0)

        CellSize = 50
        BoardMargin = 50
    
        canvas.create_line(250, 50, 250, 450, width=400, fill="green")
        for i in range(9):
            canvas.create_line(
                BoardMargin + i * CellSize, 
                BoardMargin,
                BoardMargin + i * CellSize, 
                CellSize * 8 + BoardMargin, 
                fill = "black")
            
            canvas.create_line(
                BoardMargin, 
                BoardMargin + i * CellSize,
                CellSize * 8 + BoardMargin, 
                BoardMargin + i * CellSize, 
                fill = "black")
    
        window.mainloop()
