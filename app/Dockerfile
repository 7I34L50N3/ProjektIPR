# App Dockerfile
FROM python:3.12-slim

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]