#!/bin/bash

COUNT=0
SCRIPTS=("autogames_server --game tictactoe_game --port 65432&" # server
         "autogames_client --port 65432 &" # client1
         "autogames_client --port 65432 &" # client2
        )

for ((i = 0; i < ${#SCRIPTS[@]}; i++))
do
    eval "${SCRIPTS[$i]}"
    pids[$COUNT]=$!
    COUNT=$((COUNT+1))
    sleep 0.3
done


# exit 0 only when all processes (server and client) finished with 0
# See https://stackoverflow.com/questions/356100/how-to-wait-in-bash-for-several-subprocesses-to-finish-and-return-exit-code-0
for pid in ${pids[*]}; do
    wait $pid
    if [ $? -ne 0 ]; then
        exit 1
    fi
done
