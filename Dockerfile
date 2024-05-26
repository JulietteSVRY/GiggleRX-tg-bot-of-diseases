FROM python:3.9-alpine

WORKDIR /app

COPY . /app

COPY config.json config.json

ENV CONFIG_PATH="/app/config.json"

RUN pip install -r requirements.txt


CMD ["python", "main.py"]