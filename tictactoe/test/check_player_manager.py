#!/usr/bin/env python3
#from tictactoe.scripts.PlayerManager import PlayerManager

from tictactoe.scripts.player_manager import PlayerManager

player0 = ('1271,0.0.1', 00000)  # dummy address and port
player1 = ('1271,0.0.1', 11111)  # dummy address and port
player2 = ('1271,0.0.1', 22222)  # dummy address and port
player3 = ('1271,0.0.1', 33333)  # dummy address and port
player_list = [player0, player1, player2, player3]

N_player = 3

def eq_address(ad1, ad2): # TODO: must be in utils
    for i in range(2):
        if not ad1[i] == ad2[i]:
            return False
    return True

def test_add_player():
    pm = PlayerManager(N_player)
    for n in range(N_player):
        pm.add_player(player_list[n])

    # test exceptional cases
    assert pm.add_player(player_list[0])[0] == False
    assert pm.add_player(player_list[N_player])[0] == False

def test_whos_turn_and_go_next_turn():
    pm = PlayerManager(N_player)
    for n in range(N_player):
        pm.add_player(player_list[n])

    # check turn 0
    address = pm.whos_turn()
    assert eq_address(address, player0)

    # check turn 1
    pm.go_next_turn()
    address = pm.whos_turn()
    assert eq_address(address, player1)

    # check turn 2
    pm.go_next_turn()
    address = pm.whos_turn()
    assert eq_address(address, player2)

def test_initialize(): # TODO
    pass

test_add_player()
test_whos_turn_and_go_next_turn()
