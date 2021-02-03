FROM python:3.9-slim-buster

ARG PORT=4000
ARG MAX_CONNECTIONS=30
ARG IDLE_TIME=30
ARG URL=https://drive.google.com/file/d/1C-s0ZsEtfcwA8zV3hzpjsCAsEn5Q6s_r/view?usp=sharing

COPY app /app
WORKDIR /app

RUN apt-get update && \
    apt-get -y install --no-install-recommends ncat lsof jq moreutils && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    sed -i "s/port/$PORT/g" startup.sh && \
    sed -i "s/max/$MAX_CONNECTIONS/g" startup.sh && \
    sed -i "s/idle/$IDLE_TIME/g" startup.sh && \
    jq ".url = \"$URL\"" config.json | sponge config.json && \
    chmod +x app.py

EXPOSE $PORT

ENTRYPOINT ["/bin/bash"]

CMD ["/app/startup.sh"]