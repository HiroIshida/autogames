# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

from autogames.server.games.game_manager import GameManager


class TictactoeGame(GameManager, object):

    def __init__(self, dim):
        super(TictactoeGame, self).__init__(N_player=2, dim=3)  # 2 player game
        self.stones = {}
        self.stones[1] = 1   # player1 use stone1
        self.stones[2] = -1  # player2 use stone-1

    def put(self, player_number, position):
        try:
            stone = self.stones[player_number]
        except KeyError:
            # please wait for opponent to login
            return(True, player_number[1])

        return super(TictactoeGame, self)._put(
            player_number=player_number, position=position, piece=stone)

    def show_field(self):
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
        sum_diag = 0
        for i in range(self.dim):
            sum_diag += self.field[self.dim - 1 - i][i]
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
