#!/usr/bin/env python3

from autogames.server.games.tictactoe_game import TictactoeGame

N_player = 2
player1 = ('127,0.0.1', 12345)  # dummy address and port
player2 = ('127,0.0.1', 23456)  # dummy address and port
players = range(1, N_player + 1)  # [1, 2, ... N_player]

game_field = TictactoeGame(3)
game_field.add_player()
game_field.add_player()

count = 0
for i in range(3):
    for j in range(3):
        print(game_field.show_field())
        game_field.put(players[count % 2], [i, j])
        count += 1

print(game_field.show_field())
result1 = game_field._check_checkmate(players[0])
result2 = game_field._check_checkmate(players[1])
print(result1[1])
print(result2[1])
assert game_field._check_checkmate(players[0])[0]
assert game_field._check_checkmate(players[1])[0]
