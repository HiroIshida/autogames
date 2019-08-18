#!/bin/bash

SCRIPT_DIR=$(dirname $0)

$SCRIPT_DIR/../scripts/server.py &
sleep 1
$SCRIPT_DIR/../scripts/client.py &
sleep 1
$SCRIPT_DIR/../scripts/client.py &
sleep 1
