#!/bin/bash

HERE=$(pwd)

SCRIPT_DIR=$(dirname $0)/../scripts
cd $SCRIPT_DIR

./server.py --game tictactoe_game &
sleep 1
./client.py --game tictactoe_game &
sleep 1
./client.py --game tictactoe_game &
sleep 1

cd $HERE
