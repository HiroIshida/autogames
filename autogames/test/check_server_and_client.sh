#!/bin/bash

HERE=$(pwd)

SCRIPT_DIR=$(dirname $0)/../scripts
cd $SCRIPT_DIR

autogames_server --game tictactoe_game &
sleep 1
autogames_client --game tictactoe_game &
sleep 1
autogames_client --game tictactoe_game &
sleep 1

cd $HERE
