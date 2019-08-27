import sys


class Agent:

    def __init__(self):
        self.field = None  # field state of game board

    def think(self):
        # open /dev/tty and use /dev/tty as sys.stdin (this enables user input)
        # http://nauthiz.hatenablog.com/entries/2012/03/18
        sys.stdin = file('/dev/tty')
        input_str = raw_input("please put next position (e.g. '1 2')\n")
        move = [int(s) for s in input_str.split() if s.isdigit()]

        return move
