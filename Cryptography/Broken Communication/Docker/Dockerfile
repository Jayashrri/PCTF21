FROM ubuntu:latest

ARG NCAT_HOST_PORT

RUN mkdir /app

WORKDIR /app

COPY question.py /app
COPY startup.sh /app

RUN apt-get update && \
    apt-get -y install ncat && \
    apt-get -y install python3 && \
    apt-get -y install python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install pycryptodome && \
    sed -i "s/port/$NCAT_HOST_PORT/g" /app/startup.sh && \
    chmod +x question.py
    
ENTRYPOINT ["/bin/bash"]

EXPOSE $NCAT_HOST_PORT

CMD ["/app/startup.sh"]
