# https://github.com/DenysVuika/medium-angular-docker/blob/master/Dockerfile
FROM node:21-alpine AS build
WORKDIR /solution/projects/client

COPY projects/client/tsconfig.json .
COPY projects/client/angular.json .
COPY projects/client/package.json .
COPY projects/client/yarn.lock .
COPY projects/client/Makefile .
COPY projects/client/tailwind.config.js .
RUN yarn install

COPY projects/client .
RUN yarn build

FROM nginx:1.17.1-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /solution/projects/client/dist/client /usr/share/nginx/html
