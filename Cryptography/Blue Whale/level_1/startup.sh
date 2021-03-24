#!/bin/bash

healthcheck() {
    max_retries=$1
    interval=$2

    sleep $interval
    while [ $max_retries -gt 0 ]; do
        response=$(curl --silent -w ';%{http_code}' http://localhost:3000/healthcheck)
        status=$(echo $response | rev | cut -d ';' -f 1 | rev)
        body=$(echo $response | cut -d ';' -f 1)

        if [ $status -eq 200 ] && [ "$body" == "healthy" ]; then
            echo "Level-2 passed the healthcheck."
            break
        else
            echo "Level-2 is not ready yet. Pinging again in $interval seconds..."
            max_retries=$(expr $max_retries - 1)
            sleep $interval
        fi
    done

    if [ $max_retries -eq 0 ]; then
        echo "Level-2 not ready. Aborted."
        exit 1
    fi
}

printf "\n============================================================"
printf "\nBUILDING LEVEL 2"
printf "\n============================================================\n\n"

docker-compose -f /root/level_2/docker-compose.yml up -d

healthcheck 10 60

path='/home/cobb/shell'

pip3 install -r $path/requirements.txt

chmod +x $path/main.py

chown -R cobb: $path

usermod --shell $path/main.py cobb

service ssh start

service rsyslog start

sshpass -p 'abcd' ssh -o StrictHostKeyChecking=no cobb@localhost

service fail2ban start

printf "\n============================================================"
printf "\nLEVEL 1 BUILT"
printf "\n============================================================\n\n"

/bin/bash
