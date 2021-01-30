#!/bin/bash

service ssh start

service rsyslog start

# just so that rsyslog creates /var/log/auth.log for fail2ban
sshpass -p 'abcd' ssh -o StrictHostKeyChecking=no username@localhost

service fail2ban start

/bin/bash
