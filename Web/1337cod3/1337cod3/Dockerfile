FROM node:slim

RUN apt update -y && apt upgrade -y
RUN apt install wget procps -y

RUN mkdir /home/node/app/ && chown -R node:node /home/node/app

WORKDIR /home/node

RUN wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-12/wasi-sdk-12.0-linux.tar.gz
RUN tar xvf wasi-sdk-12.0-linux.tar.gz
RUN chown -R node:node /home/node/wasi-sdk-12.0/bin

RUN apt remove wget -y

WORKDIR /home/node/app

COPY --chown=node:node . ./

USER node

RUN npm install && npm cache clean --force --loglevel=error

EXPOSE 3000
CMD [ "npm", "start"]
