from abc import ABCMeta, abstractmethod
from core import Reversi, Stone
from view import View


class ControllerBase(metaclass=ABCMeta):
    # ----- Functions to be called in view.py -----
    @abstractmethod
    def request_initialize_board(self):
        pass
    
    @abstractmethod
    def request_try_put_stone(self, coord):
        pass
    
    @abstractmethod
    def request_switch_turn(self):
        pass
    
    @abstractmethod
    def request_puttable_cells_for_current_player(self):
        pass

    @abstractmethod
    def request_get_play_mode(self):
        pass

    @abstractmethod
    def request_get_cpu_color(self):
        pass
    
    @abstractmethod
    def request_switch_mode(self, play_mode):
        pass
    
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

    @abstractmethod
    def request_notify_player_wins(self, color):
        pass
    
    @abstractmethod
    def request_notify_player_change(self, next_player_color):
        pass

    @abstractmethod
    def request_notify_draw_game(self):
        pass


class Controller(ControllerBase):
    def main(self):
        board = self.__reversi.get_board()
        self.__view.create_window(board)
    
    def __init__(self):
        self.__reversi = Reversi(self)
        self.__view = View(self)
    
    # ----- Functions to be called in view.py -----
    def request_initialize_board(self):
        self.__reversi.init_state()
        board = self.__reversi.get_board()
        self.__view.set_board(board)
        self.__view.update_highlight()

    def request_try_put_stone(self, coord):
        self.__reversi.put_stone(coord)
        self.__view.update_highlight()

    def request_switch_turn(self):
        # TODO: Switch to next turn
        pass

    def request_puttable_cells_for_current_player(self):
        color = self.__reversi.get_player_color()
        return self.__reversi.get_puttable_coords(color)
    
    def request_switch_mode(self):
        play_mode = self.__reversi.get_play_mode()
        if play_mode == Reversi.PlayMode.VsCPU:
            self.__reversi.set_play_mode(Reversi.PlayMode.VsPlayer)
        else:
            self.__reversi.set_play_mode(Reversi.PlayMode.VsCPU)

    def request_get_play_mode(self):
        return self.__reversi.get_play_mode()

    def request_get_cpu_color(self):
        return self.__reversi.get_cpu_color()

    # ----- Functions to be called in core.py -----
    def request_notify_put_fails(self, coord):
        self.__view.notify_put_fails(coord)

    def request_update_stones(self, coords, color):
        self.__view.update_stones(coords, color)

    def request_reverse_stones(self, coords):
        self.__view.reverse_stones(coords)

    def request_notify_need_pass(self):
        color = self.__reversi.get_player_color()
        color = Stone.get_rival_stone_color(color)
        self.__view.notify_need_pass(color)

    def request_notify_player_wins(self, color):
        self.__view.notify_player_wins(color)
    
    def request_notify_player_change(self, next_player_color):
        pass

    def request_notify_draw_game(self):
        pass
