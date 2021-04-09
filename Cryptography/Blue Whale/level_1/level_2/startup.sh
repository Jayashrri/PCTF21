#!/bin/bash

healthcheck() {
    max_retries=$1
    interval=$2

    sleep $interval
    while [ $max_retries -gt 0 ]; do
        response=$(curl --silent -w ';%{http_code}' http://localhost:4000/healthcheck)
        status=$(echo $response | rev | cut -d ';' -f 1 | rev)
        body=$(echo $response | cut -d ';' -f 1)

        if [ $status -eq 200 ] && [ "$body" == "healthy" ]; then
            echo "Level-3 passed the healthcheck."
            break
        else
            echo "Level-3 is not ready yet. Pinging again in $interval seconds..."
            max_retries=$(expr $max_retries - 1)
            sleep $interval
        fi
    done

    if [ $max_retries -eq 0 ]; then
        echo "Level-3 not ready. Aborted."
        exit 1
    fi
}

printf "\n============================================================"
printf "\nBUILDING LEVEL 3"
printf "\n============================================================\n\n"

docker-compose -f /root/level_3/docker-compose.yml up -d

healthcheck 8 60

pip3 install -r /root/app/requirements.txt

chown -R cobb: /home/cobb

chmod +x /home/cobb/shell/main.py

printf "\n============================================================"
printf "\nLEVEL 2 BUILT"
printf "\n============================================================\n\n"

python3 /root/app/app.py
