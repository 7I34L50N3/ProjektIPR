# Vue Dockerfile
FROM node:20-alpine

# Ustawienie katalogu roboczego
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
#RUN npm install rollup --save-dev

# Kopiowanie całego katalogu źródłowego
COPY . .

# Budowanie projektu
RUN npm run build

# Eksponowanie portu 8080
EXPOSE 8080

# Komenda do uruchomienia Vue.js
CMD ["npm", "run", "dev"]