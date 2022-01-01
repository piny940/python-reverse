from abc import ABCMeta, abstractmethod
from core import Reversi, Stone
from view import View


class ControllerBase(metaclass=ABCMeta):
    # ----- Functions to be called in view.py -----
    @abstractmethod
    # This function is suppoed to return initial board state.
    def request_initialize_board(self):
        pass
    
    @abstractmethod
    def request_try_put_stone(self, coord):
        pass
    
    @abstractmethod
    def request_switch_turn(self):
        pass
    
    # TODO: A function to switch "Player vs Player" and "Player vs CPU"
    
    # ----- Functions to be called in core.py -----
    @abstractmethod
    def request_notify_put_fails(self, coord):
        pass
    
    @abstractmethod
    def request_update_stones(self, coords, color):
        pass
    
    @abstractmethod
    def request_reverse_stones(self, coords):
        pass
    
    @abstractmethod
    def request_notify_need_pass(self):
        pass


class Controller(ControllerBase):
    def main(self):
        board = self.__reversi.get_board()
        white = self.__reversi.get_board().get_white_stones_count()
        black = self.__reversi.get_board().get_black_stones_count()
        stone_counts = {
            Stone.White: white,
            Stone.Black: black,
        }
        self.__view.create_window(board, stone_counts)
    
    def __init__(self):
        self.__reversi = Reversi(self)
        self.__view = View(self)
    
    # ----- Functions to be called in view.py -----
    def request_initialize_board(self):
        self.__reversi.init_state()
        board = self.__reversi.get_board()
        self.__view.set_board(board)

    def request_try_put_stone(self, coord):
        self.__reversi.put_stone(coord)

    def request_switch_turn(self):
        # TODO: Switch to next turn
        pass

    # ----- Functions to be called in core.py -----
    def request_notify_put_fails(self, coord):
        # TODO: Notify that the player cannot put a stone at the given coord.
        pass

    def request_update_stones(self, coords, color):
        self.__view.update_stones(coords, color)

    def request_reverse_stones(self, coords):
        self.__view.reverse_stones(coords)

    def request_notify_need_pass(self):
        # TODO: Notify that the player need to pass.
        pass

    def request_update_stone_count(self, stone_counts):
        self.__view.update_stone_counts(stone_counts)
