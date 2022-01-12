import tkinter as tk
from tkinter import messagebox
from core import Stone, Coord, Board, Reversi
import time


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
        self.__WindowWidth = 510
        self.__WindowHeight = 700

        # Board
        self.__BoardCoord = CanvasCoord(50, 200)
        self.__BoardColor = '#007300' # Green
        self.__HighlightedCellColor = '#00b000' # Light Green
        self.__CellOutlineColor = 'Black'
        self.__CellSize = 50
        self.__board = Board()

        # Stone
        self.__StoneRadius = 20
        self.__BlackStoneColor = 'Black'
        self.__WhiteStoneColor = 'White'

        # Title
        self.__TitleCoord = CanvasCoord(170, 50)
        self.__TitleSize = 50
        self.__TitleFont = 'Times'
        
        # Stone Counts Label
        self.__WhiteStoneCountsLabelCoord = CanvasCoord(90, 620)
        self.__BlackStoneCountsLabelCoord = CanvasCoord(300, 620)
        self.__StoneCountsLabelSize = 30
        self.__StoneCountsLabelFont = 'Times'
        self.__is_stones_counts_set = False
        
        # Play Mode
        self.__PlayModeLabelCoord = CanvasCoord(270, 140)
        self.__PlayModeLabelSize = 30
        self.__PlayModeLabelFont = 'Times'
        self.__is_play_mode_set = False
        
        # Current Turn Text
        self.__CurrentTurnLabelCoord = CanvasCoord(90, 140)
        self.__CurrentTurnLabelSize = 30
        self.__CurrentTurnLabelFont = 'Times'
        self.__is_current_turn_label_set = False
        
        # CPU Sleep Time
        self.__CPUSleepTime = 0.3

    def on_new_game_button_clicked(self):
        self.__controller.request_initialize_board()

    def on_switch_button_clicked(self):
        self.__controller.request_switch_mode()
        play_mode = self.__controller.request_get_play_mode()
        self.update_play_mode(play_mode)

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

    def show_stone(self, pos, color):
        str_color = ''
        if color == Stone.White:
            str_color = self.__WhiteStoneColor
        elif color == Stone.Black:
            str_color = self.__BlackStoneColor
        else:
            return
        
        self.__canvas.create_oval(
                pos.x - self.__StoneRadius,
                pos.y - self.__StoneRadius,
                pos.x + self.__StoneRadius,
                pos.y + self.__StoneRadius,
                fill = str_color)

    def update_stones(self, coords, color):
        for coord in coords:
            pos = self.coord_to_canvas_coord(coord)
            self.__board.set_stone(coord, color)
            if color == Stone.White or color == Stone.Black:
                self.show_stone(pos, color)
            else:
                self.__canvas.create_rectangle(
                    pos.x - self.__CellSize / 2, pos.y - self.__CellSize / 2,
                    pos.x + self.__CellSize / 2, pos.y + self.__CellSize / 2,
                    fill=self.__BoardColor,
                    outline=self.__CellOutlineColor
                )
        stones_counts = self.__board.get_stones_counts()
        self.update_stones_counts(stones_counts)

    def set_board(self, board):
        '''
        Update all the stones on the board.
        '''
        for x in range(Board.Size):
            for y in range(Board.Size):
                coord = Coord(x, y)
                self.update_stones([coord], board.get_stone(coord))

    def reverse_stones(self, coords):
        for coord in coords:
            color = Stone.get_rival_stone_color(self.__board.get_stone(coord))
            # You may add some animation here.
            self.update_stones([coord], color)

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

    def update_stones_counts(self, stone_counts):
        '''
        The argument 'stone_counts' is supposed to be a list that stores
        the number of white stones in the first element
        and the number of black stones in the second element
        '''
        if not self.__is_stones_counts_set:
            self.__is_stones_counts_set = True
            
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

        self.__white_stone_counts_text.set(f'White: {stone_counts[Stone.White]}')
        self.__black_stone_counts_text.set(f'Black: {stone_counts[Stone.Black]}')

    def update_play_mode(self, play_mode):
        if not self.__is_play_mode_set:
            self.__is_play_mode_set = True
            self.__play_mode_text = tk.StringVar()
            self.__play_mode_label = tk.Label(
                self.__window,
                font = f'{self.__PlayModeLabelFont} {self.__PlayModeLabelSize}',
                textvariable = self.__play_mode_text)
            self.__play_mode_label.place(
                x = self.__PlayModeLabelCoord.x,
                y = self.__PlayModeLabelCoord.y)
        
        str_play_mode = 'VS CPU  ' if play_mode == Reversi.PlayMode.VsCPU else 'VS Player'
        self.__play_mode_text.set(str_play_mode)

    def update_current_turn_label(self, current_turn_color = None):
        if current_turn_color is None:
            current_turn_color = self.__controller.request_get_play_color()
        if not self.__is_current_turn_label_set:
            self.__is_current_turn_label_set = True
            self.__current_turn_text = tk.StringVar()
            self.__current_turn_label = tk.Label(
                self.__window,
                font = f'{self.__CurrentTurnLabelFont} {self.__CurrentTurnLabelSize}',
                textvariable = self.__current_turn_text)
            self.__current_turn_label.place(
                x = self.__CurrentTurnLabelCoord.x,
                y = self.__CurrentTurnLabelCoord.y)
        
        str_current_turn = 'White' if current_turn_color == Stone.White else 'Black'
        self.__current_turn_text.set(f"{str_current_turn}'s turn")

    def update_highlight(self):
        cells_to_highlight = self.__controller.request_puttable_cells_for_current_player()
        for x in range(Board.Size):
            for y in range(Board.Size):
                coord = Coord(x, y)
                pos = self.coord_to_canvas_coord(coord)
                stone = self.__board.get_stone(coord)
                if coord in cells_to_highlight:
                    self.__canvas.create_rectangle(
                            pos.x - self.__CellSize / 2, pos.y - self.__CellSize / 2,
                            pos.x + self.__CellSize / 2, pos.y + self.__CellSize / 2,
                            fill=self.__HighlightedCellColor,
                            outline=self.__CellOutlineColor
                        )
                else:
                    self.__canvas.create_rectangle(
                            pos.x - self.__CellSize / 2, pos.y - self.__CellSize / 2,
                            pos.x + self.__CellSize / 2, pos.y + self.__CellSize / 2,
                            fill=self.__BoardColor,
                            outline=self.__CellOutlineColor
                        )
                self.show_stone(pos, stone)

    def notify_need_pass(self, color):
        str_color = ''
        if color == Stone.White:
            str_color = 'white'
        else:
            str_color = 'black'
        self.__window.update()
        messagebox.showinfo('Need pass',
            f'''
            The {str_color} player need to pass.
            Press the button to proceed to next.
            ''')

    def notify_player_wins(self, color):
        winner = ''
        if color == Stone.White:
            winner = 'white'
        elif color == Stone.Black:
            winner = 'black'
        else:
            raise BaseException()
        
        self.__window.update()
        messagebox.showinfo('Player wins',
            f'''
            The {winner} player wins.
            Press the button to start a new game.
            ''')
        self.__controller.request_initialize_board()

    def notify_put_fails(self, coord):
        self.__window.update()
        messagebox.showerror('Put fails',
            f'''
            You cannot put stone here.
            ''')

    def notify_draw_game(self):
        messagebox.showinfo('Draw', 
            f'''
            Draw Game!
            Press the button to start a new game.
            ''')
        self.__controller.request_initialize_board()

    def notify_player_change(self, next_player_color):
        self.update_current_turn_label(next_player_color)
        self.__window.update()
        if self.__controller.request_get_play_mode() == Reversi.PlayMode.VsCPU \
            and self.__controller.request_get_cpu_color() == next_player_color:
            time.sleep(self.__CPUSleepTime)

    def create_window(self, board, play_mode):
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
            fill = self.__BoardColor)

        for i in range(Board.Size + 1):
            # Vertical line
            self.__canvas.create_line(
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y,
                self.__BoardCoord.x + i * self.__CellSize,
                self.__BoardCoord.y + self.__CellSize * 8,
                fill = self.__CellOutlineColor)
            
            # Horizontal line
            self.__canvas.create_line(
                self.__BoardCoord.x,
                self.__BoardCoord.y + i * self.__CellSize,
                self.__BoardCoord.x + self.__CellSize * 8,
                self.__BoardCoord.y + i * self.__CellSize,
                fill = self.__CellOutlineColor)
        
        # ----- Stones -----
        self.set_board(board)
        
        # ---- Highlight -----
        self.update_highlight()
        
        # ---- Play Mode -----
        self.update_play_mode(play_mode)
        
        # ----- Current Turn Label -----
        self.update_current_turn_label()

        self.__window.mainloop()
