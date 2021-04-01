FROM python:3.9-slim-buster

ARG FLAG
ARG IMAGE_URL
ARG SSH_HOST
ARG SSH_PORT
ARG SSH_USERNAME
ARG SSH_USER_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG DB_ROOT_PASSWORD
ARG DB_ICECREAM_TABLE

COPY app /root/app

WORKDIR /root/app

RUN apt-get update && \
    apt-get -y install --no-install-recommends jq moreutils && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    chmod +x app.py && \
    jq ".app.flag = \"$FLAG\"" config.json | sponge config.json && \
    jq ".app.image_url = \"$IMAGE_URL\"" config.json | sponge config.json && \
    jq ".app.ssh_port = \"$SSH_HOST\"" config.json | sponge config.json && \
    jq ".app.ssh_port = \"$SSH_PORT\"" config.json | sponge config.json && \
    jq ".app.username = \"$SSH_USERNAME\"" config.json | sponge config.json && \
    jq ".app.ssh_password = \"$SSH_USER_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.host = \"$DB_HOST\"" config.json | sponge config.json && \
    jq ".db.port = \"$DB_PORT\"" config.json | sponge config.json && \
    jq ".db.database = \"$DB_NAME\"" config.json | sponge config.json && \
    jq ".db.password = \"$DB_ROOT_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.icecream_table = \"$DB_ICECREAM_TABLE\"" config.json | sponge config.json

WORKDIR /root

ENTRYPOINT ["python3"]

CMD ["/root/app/app.py"]