#!/bin/bash

LOCKFILE_PATH=/var/run/$1.pid
if [ -f $LOCKFILE_PATH ]
then
    echo "already running..."
        exit
else
    echo $$ > $LOCKFILE_PATH
    
    . ./venv/bin/activate

    python3 $1.py

    rm -f $LOCKFILE_PATH
fi


