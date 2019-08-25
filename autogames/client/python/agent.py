#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
from autogames import get_game_titles, create_message_json, read_message_json  # NOQA
import random
import socket


class Agent:

    def __init__(self, agent_port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        HOST = '127.0.0.1'
        PORT = agent_port
        self.sock.bind((HOST, PORT))
        self.sock.listen(2)

        try:
            self.connection, addr = self.sock.accept()
            print("[agent.py] [new client address]=>{}".format(addr[0]))
            print("[agent.py] [new client port]=>{}".format(addr[1]))
        except KeyboardInterrupt:
            self.sock.close()
            exit(1)

    # Main function for agent
    # Write your own algorithm here
    def think(self):
        # Sample: random algorithm
        return (random.randint(0, 2), random.randint(0, 2))


def main():
    parser = argparse.ArgumentParser(description='description of server.py')
    parser.add_argument('--agent-port', default=65432,
                        help='show all game titles which you can play')
    args = parser.parse_args()

    # communicate with client and tell the next move
    agent = Agent(int(args.agent_port))
    while True:
        # receive current field state
        bin_data = agent.connection.recv(1024)
        message = bin_data.decode()
        if message == '':
            print('[Agent] Finished.')
            exit(0)
        dict_data = read_message_json(message)
        agent.field = dict_data["field"]
        # main algorithm
        next_move = agent.think()
        # send next move
        message_json = create_message_json(
            field=None, move=next_move)
        agent.connection.sendall(message_json.encode())

    agent.sock.close()


if __name__ == "__main__":
    main()
