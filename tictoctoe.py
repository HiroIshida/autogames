class TictactoeGame:

    def __init__(self, dim):
        self.dim = dim
        self.field = [[0 for x in range(dim)] for y in range(dim)]
        self.player_address_list = []
        self.current_player_no = 0

    def set_new_player(self, player_address):
        total_player_num = len(self.player_address_list)
        if total_player_num == 2:
            return (False, "we have already two people here, sorry")
        self.player_address_list.append(player_address)
        return (True, "total player numbers is " + str(total_player_num + 1))

    def put(self, player_address, position): 
        if eq_address(player_address, self.player_address_list[0]):
            player_no = 0
        else: 
            player_no = 1

        if not player_no == self.current_player_no:
            return (False, "please wait for your opponent finish the turn")

        stone = -1 if player_no == 0 else 1

        x = position[0]
        y = position[1]

        # invalid operation
        if not self.field[x][y] == 0:
            return (False, "there is already a stone here")
        if x<0 or x >= self.dim or y < 0 or y>= self.dim:
            return (False, "out of the game field")

        # put a stone;  
        self.field[x][y] = stone
        self.current_player_no = (self.current_player_no + 1)%2
        return (True, self.get_pretty_gameboard())

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

if __name__=='__main__':
    game_field = TictactoeGame(3)
    game_field.put((0, 1))
    game_field.put((0, 2))
    game_field.put((2, 2))
    game_field.put((1, 2))
    game_field.show()

