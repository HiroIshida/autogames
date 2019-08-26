class GameManager:

    def __init__(self, N_player, dim):
        self.N_player = N_player  # how many player can join this game
        self.player_numbers = range(1, N_player + 1)  # [1, 2, ... N_player]
        self.current_players = 0  # the number of current online players
        self.counter = 0
        self.dim = dim  # size of game board (dim * dim size board)
        self.field = [[0 for x in range(dim)] for y in range(dim)]
        self.isGameFinish = False

    # piece means 'koma' or 'stone'
    def _put(self, player_number, position, piece):
        puttable = self.puttable(position)
        is_right_player = (player_number == self.whos_turn())
        is_put = False  # whether the player successfully put the piece
        # return from this method if invalid operation is executed
        if puttable and is_right_player:
            # put a stone;
            x = position[0]
            y = position[1]
            self.field[x][y] = piece
            is_put = True
        if not puttable:
            is_put = False
            print("you cannot put stone here.")
        if not is_right_player:
            is_put = False
            print("To player{}: wait your opponent to finish turn".format(
                player_number))

        # check checkmate
        result = self._check_checkmate(player_number)
        message = result[1]
        self.go_next_turn()
        # return True if the player put the piece, vice versa
        return (is_put, message)

    # You should be override this function in child class
    def puttable(self, position):
        x = position[0]
        y = position[1]
        if x < 0 or x >= self.dim or y < 0 or y >= self.dim:
            # print('out of the game field')
            return False
        elif self.field[x][y] != 0:
            # print('there is already a stone here')
            return False
        return True

    # You should be override this function in child class
    def available_positions(self, player_number):
        available_positions = []
        for i in range(self.dim):
            for j in range(self.dim):
                # invalid operation
                if self.puttable([i, j]):
                    available_positions.append([i, j])
        return available_positions

    # You should be override this function in child class
    def _check_checkmate(self, player_number):
        return (len(self.available_positions(player_number)) == 0, '')

    def add_player(self):
        print("new player is set")

        if self._isGameStart():
            return (False, "add_player: you can't join the game")

        self.current_players += 1
        return (True, "")

    def whos_turn(self):
        if not self._isGameStart():
            return (False, "whos_turn: the game hasn't started yet")
        n = self.counter % self.N_player
        return self.player_numbers[n]

    def go_next_turn(self):
        if not self._isGameStart():
            return (False, "go_next_turn: the game hasn't started yet")
        self.counter += 1

    def _isGameStart(self):
        return self.current_players == self.N_player
