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
        self.__WindowWidth = 1000
        self.__WindowHeight = 800

        # Board
        self.__BoardCoord = CanvasCoord(50, 200)
        self.__CellSize = 50

        # Title
        self.__TitleCoord = CanvasCoord(20, 10)
        self.__TitleSize = 50

    def set_menu_bar(self, window, current_mode):
        '''
        This function renews the menu bar. This function has to be called
        when the game mode switches.
        '''
        def on_new_game_button_clicked():
            # TODO: Initialize the board.
            pass

        def on_switch_button_clicked():
            # TODO: 
            # if current_mode is 'CPU Mode':
            #   Switch to Player Mode
            # elif current_mode is 'Player Mode:
            #   Switch to CPU Mode
            pass
        
        menu_bar = tk.Menu(window)
        window.config(menu=menu_bar)
        menu = tk.Menu(window)
        menu_bar.add_cascade(label='Menu', menu=menu)
        menu.add_command(label='New Game', command=on_new_game_button_clicked)
        menu.add_command(label='Switch the Mode', command=on_switch_button_clicked)
        menu_bar = tk.Menu(window)

    def get_canvas_coord_on_board(self, coord):
        x = self.__BoardCoord.x + self.__CellSize * (coord.get()[0])
        y = self.__BoardCoord.y + self.__CellSize * (coord.get()[1])
        return CanvasCoord(x, y)

    def create_window(self):
        # ----- Window & Canvas config -----
        window = tk.Tk()
        window.title("Reversi")
        window.geometry(f"{self.__WindowWidth}x{self.__WindowHeight}")

        canvas = tk.Canvas(window, width=self.__WindowWidth,
                            height=self.__WindowHeight)

        canvas.grid(row = 0, column = 0)

        # ---- Title -----
        canvas.create_text(
            self.__TitleCoord.x,
            self.__TitleCoord.y,
            text='Reversi',
            font=('', self.__TitleSize),
            anchor='nw')

        # ----- Menu Bar -----
        # TODO: self.set_menu_bar(window, mode)

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
