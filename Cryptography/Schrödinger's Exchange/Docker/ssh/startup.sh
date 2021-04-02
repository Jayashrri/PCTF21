#!/bin/bash

path="/home/username/shell"
chown -R username: $path

service ssh start

service rsyslog start

# just so that rsyslog creates /var/log/auth.log for fail2ban
sshpass -p 'abcd' ssh -o StrictHostKeyChecking=no username@localhost 1>/dev/null 2>&1

service fail2ban start

/bin/bash
