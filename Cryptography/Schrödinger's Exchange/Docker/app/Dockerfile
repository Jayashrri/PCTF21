FROM python:3.9-slim-buster

ARG APP_HOSTNAME
ARG APP_CONTAINER_PORT
ARG FLAG
ARG IMAGE_URL
ARG USER_PASSWORD
ARG DB_HOSTNAME
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_PORT
ARG DB_ICECREAM_TABLE
ARG USER_PASSWORD

COPY app ./app

WORKDIR /app

RUN apt-get update && \
    apt-get -y install --no-install-recommends jq moreutils && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    chmod +x app.py && \
    jq ".app.host = \"$APP_HOSTNAME\"" config.json | sponge config.json && \
    jq ".app.port = \"$APP_CONTAINER_PORT\"" config.json | sponge config.json && \
    jq ".app.flag = \"$FLAG\"" config.json | sponge config.json && \
    jq ".app.image_url = \"$IMAGE_URL\"" config.json | sponge config.json && \
    jq ".app.ssh_password = \"$USER_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.host = \"$DB_HOSTNAME\"" config.json | sponge config.json && \
    jq ".db.user = \"$DB_USERNAME\"" config.json | sponge config.json && \
    jq ".db.password = \"$DB_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.database = \"$DB_NAME\"" config.json | sponge config.json && \
    jq ".db.port = \"$DB_PORT\"" config.json | sponge config.json && \
    jq ".db.icecream_table = \"$DB_ICECREAM_TABLE\"" config.json | sponge config.json

WORKDIR /

ENTRYPOINT ["python3"]

CMD ["/app/app.py"]