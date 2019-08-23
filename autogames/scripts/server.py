#!/usr/bin/env python3

# as for making a server for multiple clients, see:
# https://qiita.com/1000VICKY/items/2338852a41c6aaf8efbb#4%E3%82%AF%E3%83%A9%E3%82%A4%E3%82%A2%E3%83%B3%E3%83%88%E5%81%B4%E3%81%AE%E5%8F%97%E4%BF%A1%E3%82%92%E5%88%A5%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89%E3%81%AB%E5%88%86%E9%9B%A2

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from games import get_game_titles
import socket
import json
import os
import threading
from games.tictactoe_game import TictactoeGame


class Server:

    def __init__(self, game_title):
        # you can see available game list by command below
        # python server.py --list-games or python server.py -l
        game_instances = {'tictactoe_game': TictactoeGame(3)}
        self.game_field = game_instances[game_title]

        self.client_list = []
        self.address_to_player_number = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        HOST = '127.0.0.1'
        PORT = 65431
        self.sock.bind((HOST, PORT))
        self.sock.listen(2)

    def dispatch(self, player_number, method, args):

        if method == "add_player":
            state = self.game_field.add_player()
        if method == "put":
            state = self.game_field.put(player_number, args["position"])
        if method == "get_field":
            state = self.game_field.get_field()

        return state

    def loop_handler(self, connection, player_number):
        while True:
            try:
                bin_data = connection.recv(1024)
                if not bin_data:
                    break
                str_data = bin_data.decode()
                dict_data = json.loads(str_data)

                method = dict_data["method"]
                args = dict_data["args"]
                state = self.dispatch(player_number, method, args)
                message = state[1].encode()
                connection.sendall(message)
                if state[0] is False:
                    self.sock.close()
                    os._exit(0)
                    break
            except KeyboardInterrupt:
                print("Exit from main program")
                self.sock.close()
                os._exit(1)
                break

    def main(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                print("accept new socket")
                print("[client address]=>{}".format(addr[0]))
                print("[client port]=>{}".format(addr[1]))
            except KeyboardInterrupt:
                self.sock.close()
                exit()
                break
            state = self.dispatch(addr, "add_player", {})
            isNewPlayerAccepted = state[0]
            if isNewPlayerAccepted:
                self.client_list.append((conn, addr))
                thread = threading.Thread(
                    # len(self.client_list) means player_number
                    target=self.loop_handler, args=(conn, len(self.client_list)))
                thread.start()
        self.sock.close()


if __name__ == "__main__":
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
        exit()

    # start game server
    server = Server(args.game)
    server.main()
