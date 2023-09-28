FROM node

ARG MONGODB_URI

COPY . /app
WORKDIR /app
ENV HOST='0.0.0.0'
ENV PORT='3000'
RUN npm ci
RUN npm run build:ci
CMD node ./dist/server/entry.mjs
EXPOSE 3000