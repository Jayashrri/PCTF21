FROM anuragnitt/dind:buster-slim AS base

ARG SHELL_USERNAME=cobb
ARG JAIL_USERNAME=prisoner
ARG ROOT_PASSWORD=windows-wallpaper
ARG SHELL_USER_PASSWORD=let-me-in
ARG JAIL_USER_PASSWORD=let-me-out

RUN apt-get update && \
    apt-get -y --no-install-recommends install sudo python3-pip && \
    apt-get -y autoremove && \
    useradd -m ${SHELL_USERNAME} && \
    useradd -m ${JAIL_USERNAME} && \
    echo "root:${ROOT_PASSWORD}" | chpasswd && \
    echo "${SHELL_USERNAME}:${SHELL_USER_PASSWORD}" | chpasswd && \
    echo "${JAIL_USERNAME}:${JAIL_USER_PASSWORD}" | chpasswd && \
    printf "${SHELL_USERNAME}\tALL = NOPASSWD: /bin/su - ${JAIL_USERNAME}\n" >> /etc/sudoers && \
    printf "${JAIL_USERNAME}\tALL = NOPASSWD: /usr/bin/docker\n" >> /etc/sudoers

WORKDIR /home/${JAIL_USERNAME}

RUN mkdir commands jail && \
    ln -s $(which clear) commands && \
    ln -s $(which rbash) commands && \
    ln -s $(which sudo) commands/karate && \
    ln -s $(which echo) commands/showonscreen
