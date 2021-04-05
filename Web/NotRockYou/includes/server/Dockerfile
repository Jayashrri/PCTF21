FROM node:latest

WORKDIR /usr/src/notrockyou

COPY package.json .

RUN npm i

COPY . .

CMD [ "bash", "prodserver.sh" ]