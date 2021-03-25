FROM domofactor/dind-jessie:latest AS base

ARG JAIL_USERNAME=cobb
ARG ROOT_PASSWORD=windows-wallpaper
ARG JAIL_USER_PASSWORD=let-me-out
ARG PROC_LIMIT=1000

RUN apt -y remove --purge python3.4 && \
    echo "deb http://ftp.debian.org/debian/ buster main contrib non-free" >> /etc/apt/sources.list && \
#    apt update 2>&1 1>/dev/null | sed -ne 's/.*NO_PUBKEY //p' | \
#    while read key; do if ! [[ ${keys[*]} =~ "$key" ]]; \
#    then apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 \
#    --recv-keys "$key"; keys+=("$key"); fi; done && \
    apt-get update && \
    apt-get -y --no-install-recommends install python3.7 python3-pip iproute2 build-essential file && \
    apt-get -y autoremove && \
    useradd -m ${JAIL_USERNAME} && \
    echo "root:${ROOT_PASSWORD}" | chpasswd && \
    echo "${JAIL_USERNAME}:${JAIL_USER_PASSWORD}" | chpasswd && \
    printf "\nif [ -f \"\$HOME/.bashrc\" ]; then\n\t. \"\$HOME/.bashrc\"\nfi\n" > /home/${JAIL_USERNAME}/.profile && \
    printf "*\t\t hard\t nproc\t\t ${PROC_LIMIT}\n" >> /etc/security/limits.conf

WORKDIR /home/${JAIL_USERNAME}

RUN mkdir commands jail && \
    ln -s $(which clear) commands && \
    ln -s $(which rbash) commands && \
    ln -s $(which ls) commands/uncoversecrets && \
    ln -s $(which cat) commands/meowmeow && \
    ln -s $(which echo) commands/showonscreen && \
    ln -s $(which file) commands/whatareyou
