FROM node:18-alpine

WORKDIR /app/frontend

COPY package*.json ./

RUN rm -rf node_modules package-lock.json

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3005

CMD ["npm", "run", "dev", "--", "--host"]
