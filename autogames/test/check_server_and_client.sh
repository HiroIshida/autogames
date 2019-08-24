#!/bin/bash


COUNT=0
# server
autogames_server --game tictactoe_game &
pids[$COUNT]=$!
COUNT=$((COUNT+1))
sleep 0.1
# client1
autogames_client --game tictactoe_game &
pids[$COUNT]=$!
COUNT=$((COUNT+1))
sleep 0.1
# client1
autogames_client --game tictactoe_game &
pids[$COUNT]=$!
COUNT=$((COUNT+1))
sleep 0.1

# exit 0 only when all processes (server and client) finished with 0
for pid in ${pids[*]}; do
    wait $pid
    if [ $? -ne 0 ]; then
        exit 1
    fi
done
