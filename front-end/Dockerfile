#Sample Dockerfile for NodeJS Apps

FROM node:20.18.0

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install

COPY . .

EXPOSE 8080

CMD [ "node", "front-end/server.js" ]