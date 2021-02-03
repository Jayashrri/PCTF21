FROM python:3.9-slim-buster

ARG PORT=4000
ARG MAX_CONNECTIONS=30
ARG IDLE_TIME=30

COPY app /app
WORKDIR /app

RUN apt-get update && \
    apt-get -y install --no-install-recommends ncat lsof && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    sed -i "s/port/$PORT/g" startup.sh && \
    sed -i "s/max/$MAX_CONNECTIONS/g" startup.sh && \
    sed -i "s/idle/$IDLE_TIME/g" startup.sh && \
    chmod +x app.py

EXPOSE $PORT

ENTRYPOINT ["/bin/bash"]

CMD ["/app/startup.sh"]