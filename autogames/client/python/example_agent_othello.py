#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import
import random
from autogames.server.games.othello_game import OthelloGame


class Agent:

    def __init__(self):
        self.field = None  # field state of game board
        self.game = OthelloGame(8)

    # Main function for agent
    # Write your own algorithm here
    def think(self):
        # Sample: random algorithm
        self.game.field = self.field
        # TODO: this code is messy because agent don't know the player number
        available_pos_1 = self.game.available_positions(1)
        available_pos_2 = self.game.available_positions(2)
        # if available position does not exist, return temp position
        if len(available_pos_1) == 0:
            available_pos_1 = [[-1, -1]]
        if len(available_pos_2) == 0:
            available_pos_2 = [[-2, -2]]
        choice = random.choice(
            [random.choice(available_pos_1),
             random.choice(available_pos_2)])
        return choice
