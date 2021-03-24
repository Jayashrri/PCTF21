FROM domofactor/dind-jessie:latest AS base

ARG SSH_TIMEZONE=Asia/Kolkata
ARG SSH_USERNAME=cobb
ARG JAIL_USERNAME=prisoner
ARG SSH_ROOT_PASSWORD=windows-wallpaper
ARG SSH_USER_PASSWORD=let-me-in
ARG JAIL_USER_PASSWORD=let-me-out
ARG PROC_LIMIT=1000

RUN printf "\n============================================================" && \
    printf "\nBUILDING LEVEL 1" && \
    printf "\n============================================================\n\n" && \
    ln -snf /usr/share/zoneinfo/${SSH_TIMEZONE} /etc/localtime && \
    echo ${SSH_TIMEZONE} >> /etc/timezone && \
    apt -y remove --purge python3.4 && \
    apt-get update && \
    apt-get -y --no-install-recommends install sudo openssh-server iptables fail2ban rsyslog sshpass && \
    echo "deb http://ftp.debian.org/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
#    apt update 2>&1 1>/dev/null | sed -ne 's/.*NO_PUBKEY //p' | \
#    while read key; do if ! [[ ${keys[*]} =~ "$key" ]]; \
#    then apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 \
#    --recv-keys "$key"; keys+=("$key"); fi; done && \
    apt-get update && \
    apt-get -y --no-install-recommends install python3.7 python3-pip && \
    apt-get -y autoremove && \
    useradd -m ${SSH_USERNAME} && \
    useradd -m ${JAIL_USERNAME} && \
    echo "root:${SSH_ROOT_PASSWORD}" | chpasswd && \
    echo "${SSH_USERNAME}:${SSH_USER_PASSWORD}" | chpasswd && \
    echo "${JAIL_USERNAME}:${JAIL_USER_PASSWORD}" | chpasswd && \
    printf "\nif [ -f \"\$HOME/.bashrc\" ]; then\n\t. \"\$HOME/.bashrc\"\nfi\n" > /home/${JAIL_USERNAME}/.profile && \
    printf "${SSH_USERNAME}\tALL = NOPASSWD: /bin/su - ${JAIL_USERNAME}\n" >> /etc/sudoers && \
    printf "${JAIL_USERNAME}\tALL = NOPASSWD: /usr/bin/docker\n" >> /etc/sudoers && \
    printf "*\t\t hard\t nproc\t\t ${PROC_LIMIT}\n" >> /etc/security/limits.conf

WORKDIR /home/${JAIL_USERNAME}

RUN mkdir commands jail && \
    ln -s $(which clear) commands && \
    ln -s $(which rbash) commands && \
    ln -s $(which sudo) commands/karate && \
    ln -s $(which echo) commands/showonscreen

WORKDIR /home/${SSH_USERNAME}

RUN mkdir .ssh && \
    touch .hushlogin && \
    ssh-keygen -q -t rsa -N '' -f .ssh/ssh_host_rsa_key && \
    ssh-keygen -q -t dsa -N '' -f .ssh/ssh_host_dsa_key && \
    ssh-keygen -q -t ecdsa -N '' -f .ssh/ssh_host_ecdsa_key && \
    ssh-keygen -q -t ed25519 -N '' -f .ssh/ssh_host_ed25519_key && \
    chown -R ${SSH_USERNAME}: .

WORKDIR /root
