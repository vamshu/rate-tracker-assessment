FROM node:20

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

ENV HOST=0.0.0.0
ENV WATCHPACK_POLLING=true

CMD ["npm", "run", "dev"]