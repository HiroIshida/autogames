class PlayerManager:

    def __init__(self, N_player, stone_list):
        self.N_player = N_player
        self.stone_list = stone_list
        self.player_address_list = []
        self.counter = 0

    def initialize(self):
        self.player_address_list = []

    def add_player(self, player_address):
        isAlreadySet = sum([player_address == a for a in self.player_address_list]) > 0
        if isAlreadySet:
            return (False, "add_player: you are already in the game")

        if self._isGameStart():
            return (False, "add_player: you can't join the game")

        self.player_address_list.append(player_address)

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
