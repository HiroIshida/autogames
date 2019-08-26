#!/usr/bin/env python3

from autogames.server.games.othello_game import OthelloGame
import random

N_player = 2
player1 = ('127,0.0.1', 12345)  # dummy address and port
player2 = ('127,0.0.1', 23456)  # dummy address and port
players = range(1, N_player + 1)  # [1, 2, ... N_player]

game_field = OthelloGame(8)
game_field.add_player()
game_field.add_player()

count = 0
checkmates = [False, False]  # checkmate state for each player
while True:
    player_number = players[count % 2]
    available_positions = game_field.available_positions(player_number)
    is_checkmate = game_field._check_checkmate(player_number)
    # pass
    if is_checkmate[0]:
        game_field.go_next_turn()
        checkmates[count % 2] = True
    # put stone
    else:
        print(game_field.show_field())
        game_field.put(player_number, random.choice(available_positions))
        checkmates[count % 2] = False
    count += 1
    # game end
    if all(checkmates):
        break

print(game_field.show_field())
result1 = game_field._check_checkmate(players[0])
result2 = game_field._check_checkmate(players[1])
print(result1[1])
print(result2[1])
assert game_field._check_checkmate(players[0])[0]
assert game_field._check_checkmate(players[1])[0]
