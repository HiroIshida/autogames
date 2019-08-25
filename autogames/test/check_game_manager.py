#!/usr/bin/env python3
from autogames.server.games.game_manager import GameManager

player0 = ('1271,0.0.1', 00000)  # dummy address and port
player1 = ('1271,0.0.1', 11111)  # dummy address and port
player2 = ('1271,0.0.1', 22222)  # dummy address and port
player3 = ('1271,0.0.1', 33333)  # dummy address and port
player_list = [player0, player1, player2, player3]

N_player = 3
stone_list = ["aaa", "iii", "uuu"]


def eq_address(ad1, ad2):  # TODO: must be in utils
    for i in range(2):
        if not ad1[i] == ad2[i]:
            return False
    return True


def test_add_player():
    print("test_add_player")
    gm = GameManager(N_player)
    for n in range(N_player):
        gm.add_player()

    # test exceptional cases
    assert not gm.add_player()[0]


def test_whos_turn_and_go_next_turn():
    print("test_whos_turn_and_go_next_turn")
    gm = GameManager(N_player)
    for n in range(N_player):
        gm.add_player()

    # check turn 1
    number = gm.whos_turn()
    assert number == 1

    # check turn 2
    gm.go_next_turn()
    number = gm.whos_turn()
    assert number == 2

    # check turn 3
    gm.go_next_turn()
    number = gm.whos_turn()
    assert number == 3


def test_initialize():  # TODO
    pass


test_add_player()
test_whos_turn_and_go_next_turn()
