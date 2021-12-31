import tkinter as tk
from core import Stone, Coord, Board


class CanvasCoord(Coord):
    '''
    CanvasCoord class is 2 dimention vector to express positions in the canvas.
    '''
    def __add__(self, other):
        value = super().__add__(other)
        value.__class__ = CanvasCoord
        return value

    def __sub__(self, other):
        value = super().__sub__(other)
        value.__class__ = CanvasCoord
        return value

class View:
    def __init__(self):
        # Window
        self.__WindowWidth = 1000
        self.__WindowHeight = 800

        # Board
        self.__BoardCoord = CanvasCoord(50, 200)
        self.__CellSize = 50
        self.__board = Board()

        # Stone
        self.__StoneRadius = 20

        # Title
        self.__TitleCoord = CanvasCoord(20, 10)
        self.__TitleSize = 50

    def on_new_game_button_clicked(self):
        # TODO: Initialize the board.
        pass

    def on_switch_button_clicked(self):
        # TODO:
        # if current_mode is 'CPU Mode':
        #   Switch to Player Mode
        # elif current_mode is 'Player Mode:
        #   Switch to CPU Mode
        pass

    def set_menu_bar(self, window):
        main_menu = tk.Menu(window)
        sub_menu = tk.Menu(main_menu, tearoff = 0)
        window.config(menu = main_menu)
        main_menu.add_cascade(label = "Menu", menu = sub_menu)
        sub_menu.add_command(label = "New game", 
                            command = self.on_new_game_button_clicked)
        sub_menu.add_command(label = "Switch mode", 
                            command = self.on_switch_button_clicked)

    def coord_to_canvas_coord(self, coord):
        '''
        This function converts coordinate in the board (defined in core.py)
        to coordinate in the canvas (defined in view.py).
        '''
        (coord_x, coord_y) = coord.get()
        # '0.5' has to be added to express the coords of the center of a cell.
        x = self.__BoardCoord.x + self.__CellSize * (coord_x + 0.5)
        y = self.__BoardCoord.y + self.__CellSize * (coord_y + 0.5)
        return CanvasCoord(x, y)

    def set_stone(self, canvas, coord, color):
        self.__board.set_stone(coord, color)
        pos = self.coord_to_canvas_coord(coord)
        str_color = ''
        if color == Stone.White:
            str_color = 'White'
        elif color == Stone.Black:
            str_color = 'Black'

        canvas.create_oval(
            pos.x - self.__StoneRadius,
            pos.y - self.__StoneRadius,
            pos.x + self.__StoneRadius,
            pos.y + self.__StoneRadius,
            fill = str_color)

    def set_board(self, canvas, board):
        '''
        Set all the stones in the board.
        '''
        for x in range(Board.Size):
            for y in range(Board.Size):
                coord = Coord(x, y)
                self.set_stone(canvas, coord, board.get_stone(coord))

    def reverse_stone(self, canvas, coord):
        color = Stone.get_rival_stone_color(self.__board.get_stone(coord))
        # You may add some animation here.
        self.set_stone(canvas, coord, color)

    def create_window(self):
        '''
        This function is supposed to be called when launching a game.
        '''
        # ----- Window & Canvas config -----
        self.__window = tk.Tk()
        self.__window.title("Reversi")
        self.__window.geometry(f"{self.__WindowWidth}x{self.__WindowHeight}")

        self.__canvas = tk.Canvas(self.__window, width=self.__WindowWidth,
                            height=self.__WindowHeight)

        self.__canvas.grid(row = 0, column = 0)

        # ---- Title -----
        self.__canvas.create_text(
            self.__TitleCoord.x,
            self.__TitleCoord.y,
            text='Reversi',
            font=('', self.__TitleSize),
            anchor='nw')

        # ----- Menu Bar -----
        self.set_menu_bar(self.__window)

        # ----- Board -----
        self.__canvas.create_rectangle(
            self.__BoardCoord.x,
            self.__BoardCoord.y,
            self.__BoardCoord.x + self.__CellSize * 8,
            self.__BoardCoord.y + self.__CellSize * 8,
            fill = 'green')

        for i in range(9):
            # Vertical line
            self.__canvas.create_line(
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y,
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y + self.__CellSize * 8,
                fill = 'black')
            
            # Horizontal line
            self.__canvas.create_line(
                self.__BoardCoord.x,
                self.__BoardCoord.y + i * self.__CellSize,
                self.__BoardCoord.x + self.__CellSize * 8,
                self.__BoardCoord.y + i * self.__CellSize,
                fill = 'black')

        self.__window.mainloop()
