#!/bin/bash

HERE=$(pwd)

SCRIPT_DIR=$(dirname $0)/../scripts
cd $SCRIPT_DIR

./server.py &
sleep 1
./client.py &
sleep 1
./client.py &
sleep 1

cd $HERE
