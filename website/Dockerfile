FROM node:16 AS build

# 容器内的目录，通常我们会使用 app 目录

WORKDIR /app
COPY . .
RUN npm install && npm run build
# RUN yarn && yarn build

EXPOSE 3000

CMD npm start

# FROM nginx

# WORKDIR /usr/share/nginx/html/

# COPY --from=build /app/build/* /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]

