#!/usr/bin/env python3
from autogames.server.games.game_manager import GameManager


def test_put_by_hundred_people(N_player=100):
    gm = GameManager(N_player, 10)
    # add 100 players
    for n in range(N_player):
        gm.add_player()
    print('100 players are added')
    print(gm.show_field())
    # put 1 ~ 100 stones in gm.field
    for i in range(N_player):
        player_number = gm.player_numbers[i]
        available_positions = gm.available_positions(player_number)
        gm._put(player_number, available_positions[0], player_number)
    print('100 players put stone')
    print(gm.show_field())
    # check stone number
    field_flatten = sum(gm.field, [])
    for i in range(N_player):
        player_number = gm.player_numbers[i]
        assert player_number in field_flatten, 'wrong stones in field'


test_put_by_hundred_people()
print("test_put_by_hundred_people() ended")
