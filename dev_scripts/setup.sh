#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0);pwd)
cd ${SCRIPT_DIR}/../

virtualenv virtualenv
source virtualenv/bin/activate

pip install -U pip

pip install watchdog
pip install git+https://github.com/dpallot/simple-websocket-server.git
