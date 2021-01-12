FROM node:latest

WORKDIR /usr/src/app

COPY package.json /usr/src/app

RUN npm i

COPY . /usr/src/app

EXPOSE 8000

CMD [ "npm", "start" ]