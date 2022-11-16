FROM node:16 AS build

# 容器内的目录，通常我们会使用 app 目录

WORKDIR /app
COPY . .
RUN yarn && yarn build

FROM nginx
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/build .

EXPOSE 80

