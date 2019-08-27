# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

from autogames.server.games.game_manager import GameManager
import copy


class OthelloGame(GameManager, object):

    def __init__(self, dim):
        if (dim % 2 != 0):
            print("dim size must be even.")
            return 1
        super(OthelloGame, self).__init__(N_player=2, dim=dim)  # 2 player game
        # set initial field
        self.field[dim//2 - 1][dim//2 - 1] = 1
        self.field[dim//2][dim//2] = 1
        self.field[dim//2 - 1][dim//2] = -1
        self.field[dim//2][dim//2 - 1] = -1

        self.stones = {}
        self.stones[1] = 1   # player1 use stone1
        self.stones[2] = -1  # player2 use stone-1
        print('player1: X')
        print('player2: O')

    def put(self, player_number, position):
        try:
            stone = self.stones[player_number]
        except KeyError:
            # please wait for opponent to login
            self.go_next_turn()
            return(False, player_number[1])

        # check position is available
        if position not in self.available_positions(player_number):
            self.go_next_turn()
            return(False, 'Invalid operation !')
        # put stone
        result = super(OthelloGame, self)._put(
            player_number=player_number, position=position, piece=stone)
        # reverse stone according to the rule
        self.reverse_stones(position, stone)

        return result

    def show_field(self):
        y_str_line = " "
        for x in range(self.dim):
            y_str_line += " {}".format(x)
        y_str_line += "\n"
        for y in range(self.dim):
            x_str_line = "{}|".format(y)
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

    def reverse_stones(self, position, stone):
        do_reverse = False
        dirs = [[1, 0], [1, 1], [0, 1], [-1, 1],
                [-1, 0],  [-1, -1], [0, -1], [1, -1]]
        # check 8 directions around position
        for d in dirs:
            # reverse stones in 1 direction
            stones_to_be_reversed = []
            new_x = position[0]
            new_y = position[1]
            while True:
                new_x += d[0]
                new_y += d[1]
                if new_x < 0 or new_x >= self.dim or new_y < 0 or new_y >= self.dim:
                    break
                new_stone = self.field[new_x][new_y]
                if new_stone == 0:
                    break
                elif new_stone == stone:
                    # reverse stone in queue
                    for stone_place in stones_to_be_reversed:
                        self.field[stone_place[0]][stone_place[1]] = stone
                        do_reverse = True
                    break
                else:
                    # store stones which may be reversed
                    stones_to_be_reversed.append([new_x, new_y])
        return do_reverse

    def _check_checkmate(self, player_number):
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

        # check checkmate
        if len(self.available_positions(player_number)) == 0:
            # game is over
            field_flatten = sum(self.field, [])
            my_stone_number = sum(s == stone for s in field_flatten)
            opponent_stone_number = sum(
                s == opponent_stone for s in field_flatten)
            if my_stone_number > opponent_stone_number:
                return(True, message_win)
            elif my_stone_number < opponent_stone_number:
                return(True, message_lose)
            else:
                return(True, message_draw)
        else:
            # game is in progress
            return(False, message_inprogress)

    def available_positions(self, player_number):
        stone = self.stones[player_number]
        # check puttable position
        available_positions = []
        for x in range(self.dim):
            for y in range(self.dim):
                if self.field[x][y] == 0:
                    field_old = copy.deepcopy(self.field)
                    if self.reverse_stones([x, y], stone):
                        available_positions.append([x, y])
                    self.field = field_old
        return available_positions
