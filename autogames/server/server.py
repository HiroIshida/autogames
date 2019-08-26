#!/usr/bin/env python3

# as for making a server for multiple clients, see:
# https://qiita.com/1000VICKY/items/2338852a41c6aaf8efbb#4%E3%82%AF%E3%83%A9%E3%82%A4%E3%82%A2%E3%83%B3%E3%83%88%E5%81%B4%E3%81%AE%E5%8F%97%E4%BF%A1%E3%82%92%E5%88%A5%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89%E3%81%AB%E5%88%86%E9%9B%A2

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames import get_game_titles, create_message_json, read_message_json  # NOQA
from autogames.server.games.tictactoe_game import TictactoeGame
import os
import socket
import threading
import time


class Server:

    def __init__(self, game_title, host_port):
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
        host = '127.0.0.1'
        port = host_port
        self.sock.bind((host, port))
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

    def next_move_from_player(self, connection):
        bin_data = connection.recv(1024)
        message = bin_data.decode()
        message = bin_data.decode('UTF-8')
        # remove null. To checkout, let's print(list(message))
        message = message.strip('\r\n\0')
        dict_data = read_message_json(message)
        return dict_data["move"]

    def call_and_response(self, connection, player_number):
        # wait for the other players to finish their turns
        self.wait_for_opponents(player_number)
        while True:
            # send current field to client (and then the client starts the turn)
            self.call_next_player(connection)
            # receive input from client
            next_move = self.next_move_from_player(connection)
            available_positions = self.game_field.available_positions(
                player_number)
            if next_move in available_positions:
                break
        # put next_move to the game field
        current_state = self.game_field.put(player_number, next_move)
        if current_state[0] is True:  # if the turn is successfully end
            print("player{}'s turn is end".format(player_number))
            print(self.game_field.show_field())
        else:
            print("player{} pass the turn".format(player_number))
        return current_state

    def connection_loop_with_client(self, connections, player_numbers):
        # move_players: player list who ends his turn
        move_players = [True] * self.game_field.N_player
        # start game
        is_checkmate = False
        while not is_checkmate:
            for (conn, player_number) in zip(connections, player_numbers):
                if is_checkmate:
                    break  # this is to avoid calling self.call_and_response()
                current_state = self.call_and_response(conn, player_number)
                move_players[player_number - 1] = current_state[0]
                # check whether game is end
                for player_num in self.game_field.player_numbers:
                    result = self.game_field._check_checkmate(player_num)
                    is_checkmate = (is_checkmate or result[0])
        # end game
        for player_num in self.game_field.player_numbers:
            result = self.game_field._check_checkmate(player_num)
            print(result[1])
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
    parser.add_argument('--port', default=65431,
                        help='The port address used by the server')
    args = parser.parse_args()

    # show all game titles
    if args.list_games is True:
        print('you must choose game title from below:')
        print(game_titles)
        exit(0)

    # start game server
    server = Server(args.game, int(args.port))
    while len(server.client_list) < server.game_field.N_player:
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
            print("add new player")

    connections = []
    for client in server.client_list:
        connections.append(client[0])
    server.connection_loop_with_client(
        connections, server.game_field.player_numbers)
    server.sock.close()


if __name__ == "__main__":
    main()
