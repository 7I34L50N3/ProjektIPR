# Użyj oficjalnego obrazu Node.js
FROM node:18

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . /app

# Zainstaluj zależności
RUN npm install

# Zbuduj projekt
RUN npm run build

# Serwuj aplikację za pomocą serwera npm serve
RUN npm install -g serve
CMD ["serve", "-s", "dist"]

# Otwórz port
EXPOSE 8080