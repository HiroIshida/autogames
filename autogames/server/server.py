#!/usr/bin/env python3

# as for making a server for multiple clients, see:
# https://qiita.com/1000VICKY/items/2338852a41c6aaf8efbb#4%E3%82%AF%E3%83%A9%E3%82%A4%E3%82%A2%E3%83%B3%E3%83%88%E5%81%B4%E3%81%AE%E5%8F%97%E4%BF%A1%E3%82%92%E5%88%A5%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89%E3%81%AB%E5%88%86%E9%9B%A2

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames.server.games import get_game_titles, create_message_json, read_message_json  # NOQA
from autogames.server.games.tictactoe_game import TictactoeGame
import os
import socket
import threading
import time


class Server:

    def __init__(self, game_title):
        # you can see available game list by command below
        # python server.py --list-games or python server.py -l
        game_instances = {'tictactoe_game': TictactoeGame(3)}
        self.game_field = game_instances[game_title]

        self.client_list = []
        self.address_to_player_number = {}
        self.current_player_number = 0  # this means who is the current turn
        self.lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        HOST = '127.0.0.1'
        PORT = 65431
        self.sock.bind((HOST, PORT))
        self.sock.listen(2)

    def wait_for_opponents(self, player_number):
        # wait for opponents to end their turns
        # self.current_player_number: [1, ... , N_players]
        self.lock.acquire()
        self.current_player_number += 1
        self.current_player_number %= self.game_field.N_player
        if self.current_player_number == 0:
            self.current_player_number += self.game_field.N_player
        self.lock.release()
        while self.current_player_number != player_number:
            time.sleep(0.01)

    def call_next_player(self, connection):
        message_json = create_message_json(
            field=self.game_field.field, move=None)
        connection.sendall(message_json.encode())

    def next_move_from_player(self, connection, player_number):
        bin_data = connection.recv(1024)
        message = bin_data.decode()
        dict_data = read_message_json(message)
        state = self.game_field.put(player_number, dict_data["move"])
        return state

    def connection_loop_with_client(self, connection, player_number):
        while True:
            # wait for opponents to finish the turns
            self.wait_for_opponents(player_number)
            # send current field to client
            self.call_next_player(connection)
            # receive input from client
            current_state = self.next_move_from_player(
                connection, player_number)
            print(self.game_field.show_field())
            # Game is end
            if current_state[0] is False:
                print(current_state[1])  # player-n win
                print('[Server] Finished.')
                self.sock.close()
                os._exit(0)


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

    # start game server
    server = Server(args.game)
    while True:
        try:
            # wait for clients to join this game
            conn, addr = server.sock.accept()
            print("[server.py] [new client address]=>{}".format(addr[0]))
            print("[server.py] [new client port]=>{}".format(addr[1]))
        except KeyboardInterrupt:
            server.sock.close()
            exit(1)
        state = server.game_field.add_player()
        isNewPlayerAccepted = state[0]
        if isNewPlayerAccepted:
            server.client_list.append((conn, addr))
            thread = threading.Thread(
                # len(server.client_list) means player_number
                target=server.connection_loop_with_client,
                args=(conn, len(server.client_list)))
            # thread to communicate with each client
            thread.start()
    server.sock.close()


if __name__ == "__main__":
    main()
