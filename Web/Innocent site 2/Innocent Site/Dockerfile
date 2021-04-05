FROM node:slim

RUN apt update -y && apt upgrade -y
RUN apt install dnsutils -y

RUN mkdir /home/node/app/ && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY --chown=node:node . ./

USER node

RUN npm install && npm cache clean --force --loglevel=error

EXPOSE 3000
CMD [ "npm", "start"]