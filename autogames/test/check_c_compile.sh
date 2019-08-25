#!/bin/bash

cd autogames/client/c/
gcc -Wall -g -O2 -o client-c agent.c client.c client_init.c json_utils.c -L /usr/lib/i386-linux-gnu -ljson-c
C_COMPILE=$?
rm -rf client-c
cd -
exit $C_COMPILE
