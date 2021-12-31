from abc import ABCMeta, abstractmethod
from core import Reversi
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
    def request_set_stones(self, coords, color):
        pass
    
    @abstractmethod
    def request_reverse_stones(self, coords):
        pass
    
    @abstractmethod
    def request_notify_need_pass(self):
        pass


class Controller(ControllerBase):
    def main(self):
        initial_board = self.__reversi.get_board()
        self.__view.create_window(initial_board)
        pass
    
    def __init__(self):
        self.__reversi = Reversi()
        self.__view = View(self)
    
    # ----- Functions to be called in view.py -----
    def request_initialize_board(self):
        # TODO: Instantiate board state.
        pass

    def request_try_put_stone(self, coord):
        self.__reversi.put_stone(coord)

    def request_switch_turn(self):
        # TODO: Switch to next turn
        pass

    # ----- Functions to be called in core.py -----
    def request_notify_put_fails(self, coord):
        # TODO: Notify that the player cannot put a stone at the given coord.
        pass

    def request_set_stones(self, coords, color):
        for coord in coords:
            self.__view.set_stone(coord, color)

    def request_reverse_stones(self, coords):
        pass

    def request_notify_need_pass(self):
        # TODO: Notify that the player need to pass.
        pass
