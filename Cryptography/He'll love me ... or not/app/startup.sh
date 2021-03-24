#!/bin/bash

path='/root/app'
pip3 install -r $path/requirements.txt
chmod +x $path/app.py

while true
do
    if lsof -P -i :3000 -sTCP:LISTEN > /dev/null
    then
        true
    else
        nc -l -p 3000 -k -m 30 -i 30 -e $path/app.py
    fi
    sleep 2
done
