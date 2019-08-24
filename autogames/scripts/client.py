#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames.scripts.games import get_game_titles, create_message_json, read_message_json  # NOQA
import os
import socket
import threading
import time


class Client:

    def __init__(self, game_title, agent_port):
        self.field = None  # field state of game board

        self.clients = {}
        thread_for_server = threading.Thread(
            target=self.create_socket,
            args=('127.0.0.1', 65431, 'server'))
        thread_for_agent = threading.Thread(
            target=self.create_socket,
            args=('127.0.0.1', agent_port, 'agent'))
        thread_for_server.start()
        thread_for_agent.start()

    # host: The server's hostname or IP address
    # port: The port used by the server
    def create_socket(self, host, port, socket_partner):
        self.clients[socket_partner] = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.clients[socket_partner].setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 3000)
        self.clients[socket_partner].setsockopt(
            socket.SOL_SOCKET, socket.SO_KEEPALIVE, 20)
        self.clients[socket_partner].settimeout(3)

        try:
            self.clients[socket_partner].connect((host, port))
            time.sleep(0.1)
        # catch all exception because ConnectionRefusedError is not in python 2
        # https://ja.stackoverflow.com/questions/6972/python%E3%81%A7%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E4%BE%8B%E5%A4%96%E3%82%92%E3%82%AD%E3%83%A3%E3%83%83%E3%83%81%E3%81%97-%E8%A9%B3%E7%B4%B0%E3%82%92%E8%A1%A8%E7%A4%BA%E3%81%95%E3%81%9B%E3%81%9F%E3%81%84/7008
        except Exception:
            print('Connection refused')
            exit(1)

    def send_move(self):
        # tell the current field state to agent
        message_json = create_message_json(field=self.field, move=None)
        self.clients['agent'].sendall(message_json.encode())
        # receive next move from agent
        message = self.clients['agent'].recv(1024).decode()
        next_move = read_message_json(message)['move']
        # send next move to server
        try:
            message_json = create_message_json(field=None, move=next_move)
            self.clients['server'].sendall(message_json.encode())
        except BrokenPipeError:
            print("Pipe broken")
            os._exit(1)

    def wait_for_my_turn(self):
        message = self.clients['server'].recv(1024).decode()
        if message == '':
            print('[Client] Finished.')
            exit(0)
        # receive latest field data from server
        self.field = read_message_json(message)['field']


def main():
    # pick up available game titles from scripts/games
    game_titles = get_game_titles()

    # parse command line arguments
    parser = argparse.ArgumentParser(description='description of server.py')
    parser.add_argument('-g', '--game', choices=game_titles,
                        help='set game title which you want to play')
    parser.add_argument('-l', '--list-games', action='store_true',
                        help='show all game titles which you can play')
    parser.add_argument('--agent-port', default=65432,
                        help='show all game titles which you can play')

    args = parser.parse_args()

    # show all game titles
    if args.list_games is True:
        print('you must choose game title from below:')
        print(game_titles)
        exit(0)

    # join and play the game
    client = Client(args.game, int(args.agent_port))
    while True:
        # wait until receiving current field state
        client.wait_for_my_turn()
        # execute my turn
        client.send_move()


if __name__ == '__main__':
    main()
