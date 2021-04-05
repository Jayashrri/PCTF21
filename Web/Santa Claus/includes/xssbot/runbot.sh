#!/bin/bash

while :
do
	node xssbot.js
	state=$(cat state)
	if [[ state -eq 0  ]]
	then
		echo "$(date) SLEEPING"
		sleep 5
	fi
done
