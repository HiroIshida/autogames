import json
from player_manager import PlayerManager


class TictactoeGame:

    def __init__(self, dim):
        self.dim = dim
        self.field = [[0 for x in range(dim)] for y in range(dim)]
        N_player = 2
        stone_list = [1, -1]
        self.pm = PlayerManager(N_player, stone_list)

    def set_new_player(self, player_address):
        self.pm.add_player(player_address)
        print("new player is set")

    def put(self, player_address, position):
        x = position[0]
        y = position[1]

        # invalid operation
        if x < 0 or x >= self.dim or y < 0 or y >= self.dim:
            return (False, "out of the game field")
        if not self.field[x][y] == 0:
            return (False, "there is already a stone here")

        current_turn_address, stone = self.pm.whos_turn()
        if not player_address == current_turn_address:
            return (False, "please wait for your opponent finish the turn")

        # put a stone;
        self.field[x][y] = stone
        self.pm.go_next_turn()
        return (True, self.get_pretty_gameboard())

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

    def _check_checkmate(self):
        for x in range(self.dim):
            for y in range(self.dim):
                print("hoge")


def eq_address(ad1, ad2):
    for i in range(2):
        if not ad1[i] == ad2[i]:
            return False
    return True
