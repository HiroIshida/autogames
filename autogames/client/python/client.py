#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames import get_game_titles, create_message_json, read_message_json  # NOQA
from importlib import import_module
import os
import socket
import time


class Client:

    def __init__(self, host_port, agent_file, timeout):
        # import agent
        agent = import_module("autogames.client.python." + agent_file)
        self.agent = agent.Agent()  # game agent

        host = '127.0.0.1'  # The server's hostname or IP address
        port = host_port   # The port used by the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.settimeout(timeout)
        self.client.connect((host, port))

    def send_move(self):
        # receive next move from agent
        next_move = self.agent.think()
        # send next move to server
        try:
            message_json = create_message_json(field=None, move=next_move)
            self.client.sendall(message_json.encode())
        except Exception:
            # BrokenPipeError is not defined in Python 2.x
            print("BrokenPipeError")
            os._exit(1)

    def wait_for_my_turn(self):
        message = self.client.recv(1024).decode()
        if message == '':
            print('[Python Client] Finished.')
            exit(0)
        # receive latest field data from server
        self.agent.field = read_message_json(message)['field']


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='description of server.py')
    parser.add_argument('--port', default=65431,
                        help='The port address used by the server')
    parser.add_argument('--agent-file', default='agent',
                        help='The file name which contains Agent class')
    parser.add_argument('--timeout', default='3',
                        help='timeout of client input')
    args = parser.parse_args()

    # join and play the game
    client = Client(int(args.port), args.agent_file, int(args.timeout))
    while True:
        time.sleep(0.1)
        # wait until receiving current field state
        client.wait_for_my_turn()
        # execute my turn
        client.send_move()


if __name__ == '__main__':
    main()
