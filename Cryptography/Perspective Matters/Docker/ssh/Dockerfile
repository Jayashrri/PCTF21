FROM ubuntu:latest

ARG TIMEZONE
ARG USERNAME
ARG ROOT_PASSWORD
ARG USER_PASSWORD

RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
    echo $TIMEZONE > /etc/timezone && \
    apt-get update && \
    apt-get -y install --no-install-recommends openssh-server && \
    rm /etc/ssh/sshd_config

COPY sshd_config /etc/ssh
COPY startup.sh /root

RUN chmod +x /root/startup.sh && \
    sed -i "s/username/$USERNAME/g" /etc/ssh/sshd_config && \
    useradd -m $USERNAME && \
    echo "root:$ROOT_PASSWORD" | chpasswd && \
    echo "$USERNAME:$USER_PASSWORD" | chpasswd

USER $USERNAME

WORKDIR /home/$USERNAME

COPY file.pdf .

RUN mkdir .ssh && \
    ssh-keygen -q -t rsa -N '' -f ./.ssh/ssh_host_rsa_key && \
    ssh-keygen -q -t dsa -N '' -f ./.ssh/ssh_host_dsa_key && \
    ssh-keygen -q -t ecdsa -N '' -f ./.ssh/ssh_host_ecdsa_key && \
    ssh-keygen -q -t ed25519 -N '' -f ./.ssh/ssh_host_ed25519_key

USER root

WORKDIR /root

ENTRYPOINT ["/bin/bash"]

CMD ["./startup.sh"]
