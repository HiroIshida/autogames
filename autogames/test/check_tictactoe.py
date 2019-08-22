#!/usr/bin/env python3

from autogames.scripts.games.tictactoe_game import TictactoeGame


player1 = ('127,0.0.1', 12345)  # dummy address and port
player2 = ('127,0.0.1', 23456)  # dummy address and port
players = [player1, player2]

game_field = TictactoeGame(3)
game_field.set_new_player(player1)
game_field.set_new_player(player2)

count = 0
for i in range(3):
    for j in range(3):
        game_field.put(players[count % 2], (i, j))
        count += 1

print(game_field.get_pretty_gameboard())
