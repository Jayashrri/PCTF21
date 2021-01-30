FROM ubuntu:latest

ARG TIMEZONE
ARG USERNAME
ARG ROOT_PASSWORD
ARG USER_PASSWORD
ARG DB_HOSTNAME
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_PORT
ARG DB_ID_TABLE
ARG DB_ICECREAM_TABLE
ARG ADMIN_USERNAME
ARG ADMIN_EMAIL
ARG ADMIN_PASSWORD

RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
    echo $TIMEZONE > /etc/timezone && \
    apt-get update && \
    apt-get -y install openssh-server python3-pip jq moreutils fail2ban rsyslog sshpass

RUN rm /etc/ssh/sshd_config

COPY sshd_config /etc/ssh
COPY jail.local /etc/fail2ban
COPY startup.sh /root

RUN chmod +x /root/startup.sh && \
    sed -i "s/username/$USERNAME/g" /root/startup.sh && \
    sed -i "s/username/$USERNAME/g" /etc/ssh/sshd_config && \
    useradd -m $USERNAME && \
    echo "root:$ROOT_PASSWORD" | chpasswd && \
    echo "$USERNAME:$USER_PASSWORD" | chpasswd

WORKDIR /home/$USERNAME

COPY shell ./shell

WORKDIR /home/$USERNAME/shell

RUN pip3 install -r requirements.txt && \
    jq ".db.host = \"$DB_HOSTNAME\"" config.json | sponge config.json && \
    jq ".db.user = \"$DB_USERNAME\"" config.json | sponge config.json && \
    jq ".db.password = \"$DB_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.database = \"$DB_NAME\"" config.json | sponge config.json && \
    jq ".db.port = \"$DB_PORT\"" config.json | sponge config.json && \
    jq ".db.id_table = \"$DB_ID_TABLE\"" config.json | sponge config.json && \
    jq ".db.icecream_table = \"$DB_ICECREAM_TABLE\"" config.json | sponge config.json && \
    jq ".admin.username = \"$ADMIN_USERNAME\"" config.json | sponge config.json && \
    jq ".admin.email = \"$ADMIN_EMAIL\"" config.json | sponge config.json && \
    HASH=$(python3 -c "import bcrypt; print(bcrypt.hashpw(b'$ADMIN_PASSWORD', bcrypt.gensalt()).decode())") && \
    jq ".admin.password = \"$HASH\"" config.json | sponge config.json && \
    echo "/home/$USERNAME/shell/main.py" >> /etc/shells && \
    chown -R $USERNAME: .

USER $USERNAME

WORKDIR /home/$USERNAME

RUN touch .hushlogin && \
    chmod +x ./shell/main.py && \
    mkdir .ssh && \
    ssh-keygen -q -t rsa -N '' -f ./.ssh/ssh_host_rsa_key && \
    ssh-keygen -q -t dsa -N '' -f ./.ssh/ssh_host_dsa_key && \
    ssh-keygen -q -t ecdsa -N '' -f ./.ssh/ssh_host_ecdsa_key && \
    ssh-keygen -q -t ed25519 -N '' -f ./.ssh/ssh_host_ed25519_key

USER root

WORKDIR /root

RUN usermod --shell /home/$USERNAME/shell/main.py $USERNAME

ENTRYPOINT ["/bin/bash"]

CMD ["./startup.sh"]