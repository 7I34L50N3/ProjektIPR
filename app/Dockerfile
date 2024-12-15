# Użyj oficjalnego obrazu Pythona
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . /app

# Zainstaluj zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Otwórz port dla Flask
EXPOSE 5000

# Komenda startowa
CMD ["python", "app.py"]

