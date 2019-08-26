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
        # return from this method if invalid operation is executed
        if not self.puttable(position):
            return(True, "invalid operation")

        current_turn_player = self.whos_turn()
        if not player_number == current_turn_player:
            return (True, "please wait your opponent for finishing the turn")

        # put a stone;
        x = position[0]
        y = position[1]
        self.field[x][y] = piece

        # check checkmate
        result = self._check_checkmate(player_number)
        isGameEnd = result[0]
        message = result[1]

        if not isGameEnd:
            self.go_next_turn()
        return (not isGameEnd, message)

    def puttable(self, position):
        x = position[0]
        y = position[1]
        if x < 0 or x >= self.dim or y < 0 or y >= self.dim:
            print('out of the game field')
            return False
        elif self.field[x][y] != 0:
            print('there is already a stone here')
            return False
        return True

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

    # methods which must be override in child classes
    # @abstractmethod
    def put(self, player_number, position):
        pass

    # @abstractmethod
    def get_field(self):
        pass

    # @abstractmethod
    def show_field(self):
        pass
