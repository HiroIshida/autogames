class TwoPlayerGame:

    def __init__(self):
        self.state = None
        self.player_address_list = []
        self.stone_list = [1, -1]
        self.counter = 0
        self.N_player = 2

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
        return address, self.stone_list[n]

    def go_next_turn(self):
        if not self._isGameStart():
            return (False, "go_next_turn: the game hasn't started yet")
        self.counter += 1

    def _isGameStart(self):
        return len(self.player_address_list) == self.N_player

    def get_state(self):
        self.state
