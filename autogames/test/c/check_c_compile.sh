#!/bin/bash

cd autogames/client/c/
make client_c AGENT_FILE=example_agent_tictactoe.c
C_COMPILE=$?
rm -rf client_c
cd -
exit $C_COMPILE
