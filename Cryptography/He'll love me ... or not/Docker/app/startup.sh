#!/bin/bash

while true
do
    if lsof -P -i :port -sTCP:LISTEN > /dev/null
    then
        true
    else
        nc -l -p port -k -m max -i idle -e /app/app.py
    fi
    sleep 2
done
