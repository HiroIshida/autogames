# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import json
from autogames.scripts.games.game_manager import GameManager


class TictactoeGame(GameManager, object):

    def __init__(self, dim):
        super(TictactoeGame, self).__init__(2)  # 2 player game
        self.dim = dim
        self.field = [[0 for x in range(dim)] for y in range(dim)]
        self.isGameFinish = False

    def put(self, player_number, position):
        x = position[0]
        y = position[1]

        # invalid operation
        if x < 0 or x >= self.dim or y < 0 or y >= self.dim:
            return (True, "out of the game field")
        if not self.field[x][y] == 0:
            return (True, "there is already a stone here")

        current_turn_player, player_number = self.whos_turn()
        if player_number == 1:
            stone = 1
        elif player_number == 2:
            stone = -1

        if not player_number == current_turn_player:
            return (True, "please wait for your opponent finish the turn")

        # put a stone;
        self.field[x][y] = stone
        self.go_next_turn()

        # check checkmate
        result = self._check_checkmate(stone, x, y)
        isGameEnd = result[0]
        message = result[1] + "\n" + self.get_pretty_gameboard()
        return (not isGameEnd, message)

    def get_field(self):
        list_data = self.field
        dict_data = {'data': list_data}
        str_data = json.dumps(dict_data)
        return (True, str_data)

    def get_pretty_gameboard(self):
        y_str_line = ""
        for y in range(self.dim):
            x_str_line = "|"
            for x in range(self.dim):
                stone = self.field[x][y]
                if stone == 0:
                    str_stone = " |"
                elif stone == -1:
                    str_stone = "O|"
                else:
                    str_stone = "X|"
                x_str_line += str_stone

            y_str_line += (x_str_line + "\n")
        return y_str_line

    def _check_checkmate(self, stone, x, y):
        # check checkmate in a sequential (NOT batch) manner
        # by calling only when players put a stone.

        message_win = "you win"
        message_draw = "draw"
        message_inprogress = ""

        # check horizontal (x)
        sum_x = 0
        for i in range(self.dim):
            sum_x += self.field[x][i]
        if sum_x == stone * 3:
            return (True, message_win)

        # check vertical (y)
        sum_y = 0
        for i in range(self.dim):
            sum_y += self.field[i][y]
        if sum_y == stone * 3:
            return (True, message_win)

        # check diagonal
        sum_diag = 0
        for i in range(self.dim):
            sum_diag += self.field[i][i]
        if sum_diag == stone * 3:
            return (True, message_win)

        # check whether the field is full or not
        field_flatten = sum(self.field, [])
        is_field_full = all(elem != 0 for elem in field_flatten)
        if is_field_full:
            return (True, message_draw)

        return (False, message_inprogress)
