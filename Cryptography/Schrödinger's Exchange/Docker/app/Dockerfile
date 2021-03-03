FROM python:3.9-slim-buster

ARG FLAG
ARG IMAGE_URL
ARG USER_PASSWORD
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_ICECREAM_TABLE
ARG USER_PASSWORD

COPY app ./app

WORKDIR /app

RUN apt-get update && \
    apt-get -y install --no-install-recommends jq moreutils && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    chmod +x app.py && \
    jq ".app.flag = \"$FLAG\"" config.json | sponge config.json && \
    jq ".app.image_url = \"$IMAGE_URL\"" config.json | sponge config.json && \
    jq ".app.ssh_password = \"$USER_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.password = \"$DB_PASSWORD\"" config.json | sponge config.json && \
    jq ".db.database = \"$DB_NAME\"" config.json | sponge config.json && \
    jq ".db.icecream_table = \"$DB_ICECREAM_TABLE\"" config.json | sponge config.json

WORKDIR /

ENTRYPOINT ["python3"]

CMD ["/app/app.py"]