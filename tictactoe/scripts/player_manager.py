class PlayerManager:

    def __init__(self, N_player):
        print("hoge")
        self.N_player = N_player
        self.player_address_list = []
        #self.current_player_address = None # will be set only after all players enter the game field; see add_player
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
        print("hoge")
        if not self._isGameStart():
            return (False, "whos_turn: the game hasn't started yet")
        n = self.counter % self.N_player
        address = self.player_address_list[n]
        return address

    def go_next_turn(self):
        if not self._isGameStart():
            return (False, "go_next_turn: the game hasn't started yet")
        self.counter += 1
        return 

    def _isGameStart(self):
        return len(self.player_address_list) == self.N_player

