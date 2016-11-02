#!/bin/bash

HOME=$(cd $(dirname $0);pwd)

cd ${HOME}
source ../virtualenv/bin/activate

python autoreloadserver.py $*
