FROM node:latest

WORKDIR /usr/src/app

COPY package.json .

RUN npm i

COPY . .


CMD [ "./runbot.sh" ]