class GameManager:

    def __init__(self, N_player, player_numbers):
        self.N_player = N_player
        self.player_numbers = player_numbers
        self.player_address_list = []
        self.counter = 0

    def initialize(self):
        self.player_address_list = []

    def add_player(self, player_address):
        print("new player is set")
        isAlreadySet = sum(
            [player_address == a for a in self.player_address_list]) > 0
        if isAlreadySet:
            return (False, "add_player: you are already in the game")

        if self._isGameStart():
            return (False, "add_player: you can't join the game")

        self.player_address_list.append(player_address)
        return (True, "")

    def whos_turn(self):
        if not self._isGameStart():
            return (False, "whos_turn: the game hasn't started yet")
        n = self.counter % self.N_player
        address = self.player_address_list[n]
        return address, self.player_numbers[n]

    def go_next_turn(self):
        if not self._isGameStart():
            return (False, "go_next_turn: the game hasn't started yet")
        self.counter += 1

    def _isGameStart(self):
        return len(self.player_address_list) == self.N_player

    # methods which must be override in child classes
    @abstractmethod
    def put(self, player_address, position):
        pass

    @abstractmethod
    def get_field(self):
        pass

    @abstractmethod
    def check_checkmate_field(self, stone, x, y):
        pass
