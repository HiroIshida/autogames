#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import
import random


class Agent:

    def __init__(self):
        self.field = None  # field state of game board

    # Main function for agent
    # Write your own algorithm here
    def think(self):
        # Sample: random algorithm
        return (random.randint(0, 2), random.randint(0, 2))
