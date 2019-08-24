#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames.scripts.games import get_game_titles, create_message_json, read_message_json  # NOQA
from autogames.scripts.games.tictactoe_game import TictactoeGame
import os
import socket
import time


class Client:

    def __init__(self, game_title):
        # you can see available game list by command below
        # python client.py --list-games or python client.py -l
        game_instances = {'tictactoe_game': TictactoeGame(3)}
        self.game_field = game_instances[game_title]

        self.host = '127.0.0.1'  # The server's hostname or IP address
        self.port = 65431        # The port used by the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.settimeout(3)
        try:
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            print('Connection refused')
            exit(1)

    def send_move(self, position):
        try:
            message_json = create_message_json(field=None, move=position)
            self.client.sendall(message_json.encode())
        except BrokenPipeError:
            print("Pipe broken")
            os._exit(1)

    def wait_for_my_turn(self):
        message = self.client.recv(1024).decode()
        if message == '':
            print('[Client] Finished.')
            exit(0)
        # receive latest field data from server
        self.game_field.field = read_message_json(message)['field']

    def join_game(self):
        while True:
            time.sleep(0.1)
            # wait until receiving current field state
            self.wait_for_my_turn()
            # execute my turn
            self.send_move(self.game_field.think())


def main():
    # pick up available game titles from scripts/games
    game_titles = get_game_titles()

    # parse command line arguments
    parser = argparse.ArgumentParser(description='description of server.py')
    parser.add_argument('-g', '--game', choices=game_titles,
                        help='set game title which you want to play')
    parser.add_argument('-l', '--list-games', action='store_true',
                        help='show all game titles which you can play')
    args = parser.parse_args()

    # show all game titles
    if args.list_games is True:
        print('you must choose game title from below:')
        print(game_titles)
        exit(0)

    client = Client(args.game)
    client.join_game()


if __name__ == '__main__':
    main()
