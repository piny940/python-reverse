import tkinter as tk
from tkinter import messagebox
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
    def __init__(self, controller):
        self.__controller = controller
        
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
        self.__TitleFont = 'Times'
        
        # Stone Counts Label
        self.__WhiteStoneCountsLabelCoord = CanvasCoord(600, 400)
        self.__BlackStoneCountsLabelCoord = CanvasCoord(600, 450)
        self.__StoneCountsLabelSize = 25
        self.__StoneCountsLabelFont = 'Times'

    def on_new_game_button_clicked(self):
        self.__controller.request_initialize_board()

    def on_switch_button_clicked(self):
        # TODO:
        # if current_mode is 'CPU Mode':
        #   Switch to Player Mode
        # elif current_mode is 'Player Mode:
        #   Switch to CPU Mode
        pass

    def set_menu_bar(self):
        main_menu = tk.Menu(self.__window)
        sub_menu = tk.Menu(main_menu, tearoff = 0)
        self.__window.config(menu = main_menu)
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

    def canvas_coord_to_coord(self, canvas_coord):
        if not self.is_coord_on_board(canvas_coord):
            '''
            Convert a coord on canvas to the corresponding coord on reversi board.
            canvas_coord must point inside of the reversi board.
            If not, this function raises an exception.
            '''
            raise BaseException()
        
        x = (canvas_coord.x - self.__BoardCoord.x) // self.__CellSize
        y = (canvas_coord.y - self.__BoardCoord.y) // self.__CellSize
        return Coord(x, y)

    def update_stones(self, coords, color):
        for coord in coords:
            self.__board.set_stone(coord, color)
            pos = self.coord_to_canvas_coord(coord)
            str_color = ''
            if color == Stone.White:
                str_color = 'White'
            elif color == Stone.Black:
                str_color = 'Black'
            else:
                self.__canvas.create_rectangle(
                    pos.x - self.__CellSize / 2, pos.y - self.__CellSize / 2,
                    pos.x + self.__CellSize / 2, pos.y + self.__CellSize / 2,
                    fill='Green',
                    outline='Black'
                )
                return

            self.__canvas.create_oval(
                pos.x - self.__StoneRadius,
                pos.y - self.__StoneRadius,
                pos.x + self.__StoneRadius,
                pos.y + self.__StoneRadius,
                fill = str_color)

    def set_board(self, board):
        '''
        Update all the stones on the board.
        '''
        for x in range(Board.Size):
            for y in range(Board.Size):
                coord = Coord(x, y)
                self.update_stone(coord, board.get_stone(coord))

    def reverse_stones(self, coords):
        for coord in coords:
            color = Stone.get_rival_stone_color(self.__board.get_stone(coord))
            # You may add some animation here.
            self.update_stone(coord, color)

    def is_coord_on_board(self, canvas_coord):
        board_size = self.__CellSize * Board.Size
        return (
            self.__BoardCoord.x <= canvas_coord.x 
                <= self.__BoardCoord.x + board_size
            and
            self.__BoardCoord.y <= canvas_coord.y
                <= self.__BoardCoord.y + board_size
        )

    def on_canvas_clicked(self, event):
        canvas_coord = CanvasCoord(event.x, event.y)
        if self.is_coord_on_board(canvas_coord):
            coord = self.canvas_coord_to_coord(canvas_coord)
            self.__controller.request_try_put_stone(coord)
            return

    def set_stones_counts(self, stone_counts):
        '''
        The argument 'stone_counts' is supposed to be a list that stores
        the number of white stones in the first element
        and the number of black stones in the second element
        '''
        # White stone counts
        self.__white_stone_counts_text = tk.StringVar()
        self.__white_stone_counts_label = tk.Label(
            self.__window,
            font = f'{self.__StoneCountsLabelFont} {self.__StoneCountsLabelSize}',
            textvariable = self.__white_stone_counts_text)
        self.__white_stone_counts_label.place(
            x = self.__WhiteStoneCountsLabelCoord.x,
            y = self.__WhiteStoneCountsLabelCoord.y)
        
        # Black stone counts
        self.__black_stone_counts_text = tk.StringVar()
        self.__black_stone_counts_label = tk.Label(
            self.__window,
            font = f'{self.__StoneCountsLabelFont} {self.__StoneCountsLabelSize}',
            textvariable = self.__black_stone_counts_text)
        self.__black_stone_counts_label.place(
            x = self.__BlackStoneCountsLabelCoord.x,
            y = self.__BlackStoneCountsLabelCoord.y)
        
        self.update_stone_counts(stone_counts)
        
    def update_stone_counts(self, stone_counts):
        self.__white_stone_counts_text.set(f'White: {stone_counts[Stone.White]}')
        self.__black_stone_counts_text.set(f'Black: {stone_counts[Stone.Black]}')

    def update_highlight(self, cells_to_highlight):
        pass

    def notify_need_pass(self, cells_to_highlight):
        messagebox.showinfo('Need pass', 'You need to pass')
        self.update_highlight(cells_to_highlight)

    def create_window(self, initial_board, initial_stone_counts, highlighted_cells):
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
        self.__canvas.bind('<ButtonPress-1>', self.on_canvas_clicked)

        # ---- Title -----
        self.__canvas.create_text(
            self.__TitleCoord.x,
            self.__TitleCoord.y,
            text='Reversi',
            font=(self.__TitleFont, self.__TitleSize),
            anchor='nw')

        # ----- Menu Bar -----
        self.set_menu_bar()

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
        
        # ----- Stones -----
        self.set_board(initial_board)
        
        # ----- Stone counts -----
        self.set_stones_counts(initial_stone_counts)
        
        # ---- Highlight -----
        self.update_highlight(highlighted_cells)

        self.__window.mainloop()
