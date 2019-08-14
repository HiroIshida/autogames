class TictactoeGame:

    def __init__(self, dim):
        self.dim = dim
        self.field = [[0 for x in range(dim)] for y in range(dim)]
        self.player_no = 0

    def put(self, position): 
        if self.player_no == 0:
            stone = -1 # X
        else:
            stone = 1 # O

        x = position[0]
        y = position[1]

        # invalid operation
        if not self.field[x][y] == 0:
            return False
        if x<0 or x >= self.dim or y < 0 or y>= self.dim:
            return False

        # put a stone;  
        self.field[x][y] = stone
        self.player_no = (self.player_no + 1)%2
        return True

    def get_player_no(self):
        return self.player_no

    def show(self):
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
        print(y_str_line)

    def _check_checkmate(self):
        for x in range(self.dim):
            for y in range(self.dim):
                print("hoge")



if __name__=='__main__':
    game_field = TictactoeGame(3)
    game_field.put((0, 1))
    game_field.put((0, 2))
    game_field.put((2, 2))
    game_field.put((1, 2))
    game_field.show()

