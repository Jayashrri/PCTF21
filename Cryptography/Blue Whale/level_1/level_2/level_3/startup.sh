#!/bin/bash

pip3 install -r /root/app/requirements.txt

ln -s /home/cobb/jail/keys /home/cobb/commands

chown -R cobb: /home/cobb

chattr -R +i /home/cobb/jail

printf "\n============================================================"
printf "\nLEVEL 3 BUILT"
printf "\n============================================================\n\n"

python3 /root/app/app.py
