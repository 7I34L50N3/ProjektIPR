# App Dockerfile
FROM python:3.12-bullseye

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

WORKDIR /app

# Instalacja brakujących pakietów
RUN apt-get update && apt-get install -y \
    apt-utils \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    tzdata \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]