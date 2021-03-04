FROM python:3.9-slim-buster

RUN mkdir /root/app && \
    apt-get update && \
    apt-get -y install --no-install-recommends ncat lsof && \
    pip3 install --upgrade pip

ENTRYPOINT ["/bin/bash"]

CMD ["/root/app/startup.sh"]