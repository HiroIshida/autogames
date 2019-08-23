class GameManager:

    def __init__(self, N_player):
        self.N_player = N_player  # how many player can join this game
        self.player_numbers = range(1, N_player + 1)  # [1, 2, ... N_player]
        self.current_players = 0  # the number of current online players
        self.counter = 0

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
        number = self.player_numbers[n]
        return number, self.player_numbers[n]

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
    def check_checkmate_field(self, stone, x, y):
        pass
