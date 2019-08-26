#!/bin/bash

COUNT=0
SCRIPTS=("autogames_server --game othello_game --port 65432 &" # server
         "python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello &" # client1 of python
         "python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello &" # client2 of python
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
