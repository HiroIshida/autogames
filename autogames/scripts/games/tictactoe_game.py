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
        self.stones = {}
        self.stones[1] = 1   # player1 use stone1
        self.stones[2] = -1  # player2 use stone-1

    def put(self, player_number, position):
        # return from this method if invalid operation is executed
        x = position[0]
        y = position[1]
        if not position in self.available_positions():
            if x < 0 or x >= self.dim or y < 0 or y >= self.dim:
                print("out of the game field")
            else:
                print("there is already a stone here")
            return(True, 'Invalid operation !')

        current_turn_player = self.whos_turn()
        try:
            stone = self.stones[current_turn_player]
        except KeyError:
            return(True, current_turn_player[1])  # please wait for opponent to login

        if not player_number == current_turn_player:
            return (True, "please wait your opponent for finishing the turn")

        # put a stone;
        self.field[x][y] = stone

        # check checkmate
        result = self._check_checkmate(player_number)
        isGameEnd = result[0]
        message = result[1] + "\n" + self.get_pretty_gameboard()

        if not isGameEnd:
            self.go_next_turn()
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

    def _check_checkmate(self, player_number):
        # check checkmate in a sequential (NOT batch) manner
        # by calling only when players put a stone.

        message_win = "player" + str(player_number) + " win"
        message_lose = "player" + str(player_number) + " lose"
        message_draw = "draw"
        message_inprogress = ""

        stone = self.stones[player_number]
        if player_number == 1:
            opponent_player_number = 2
        elif player_number == 2:
            opponent_player_number = 1
        opponent_stone = self.stones[opponent_player_number]

        # check horizontal (x)
        for y in range(self.dim):
            sum_x = 0
            for x in range(self.dim):
                sum_x += self.field[x][y]
            if sum_x == stone * 3:
                return (True, message_win)
            elif sum_x == opponent_stone * 3:
                return (True, message_lose)
        # check vertical (y)
        for x in range(self.dim):
            sum_y = 0
            for y in range(self.dim):
                sum_y += self.field[x][y]
            if sum_y == stone * 3:
                return (True, message_win)
            elif sum_y == opponent_stone * 3:
                return (True, message_lose)

        # check diagonal
        sum_diag = 0
        for i in range(self.dim):
            sum_diag += self.field[i][i]
        if sum_diag == stone * 3:
            return (True, message_win)
        elif sum_diag == opponent_stone * 3:
            return (True, message_lose)

        # check whether the field is full or not
        field_flatten = sum(self.field, [])
        is_field_full = all(elem != 0 for elem in field_flatten)
        if is_field_full:
            return (True, message_draw)

        return (False, message_inprogress)

    def available_positions(self):
        available_positions = []
        for i in range(self.dim):
            for j in range(self.dim):
                # invalid operation
                if self.field[i][j] == 0:
                    available_positions.append([i, j])
        return available_positions
