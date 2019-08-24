#!/bin/bash

COUNT=0
SCRIPTS=("autogames_server --game tictactoe_game &" # server
         "python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65432 &" # agent for client1
         "autogames_client --game tictactoe_game --agent-port 65432 &" # client1
         "python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65433 &" # agent for client1
         "autogames_client --game tictactoe_game --agent-port 65433 &" # client2
        )

for ((i = 0; i < ${#SCRIPTS[@]}; i++))
do
    eval "${SCRIPTS[$i]}"
    pids[$COUNT]=$!
    COUNT=$((COUNT+1))
    sleep 0.01
done


# for script in ${SCRIPTS[@]}; do
#     echo ${script}
#     pids[$COUNT]=$!
#     COUNT=$((COUNT+1))
#     sleep 0.1
# done

# # server
# # autogames_server --game tictactoe_game &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # client1
# # python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65432 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # autogames_client --game tictactoe_game --agent-port 65432 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # client2
# # python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65433 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # autogames_client --game tictactoe_game --agent-port 65433 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1


###

# COUNT=0

# # server
# autogames_server --game tictactoe_game &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # client1
# python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65432 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# autogames_client --game tictactoe_game --agent-port 65432 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# # client2
# python autogames/scripts/agents/tictactoe_game/agent.py --agent-port 65433 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1
# autogames_client --game tictactoe_game --agent-port 65433 &
# pids[$COUNT]=$!
# COUNT=$((COUNT+1))
# sleep 0.1

###

# exit 0 only when all processes (server and client) finished with 0
# See https://stackoverflow.com/questions/356100/how-to-wait-in-bash-for-several-subprocesses-to-finish-and-return-exit-code-0
for pid in ${pids[*]}; do
    wait $pid
    if [ $? -ne 0 ]; then
        exit 1
    fi
done
