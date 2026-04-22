FROM python:3-bookworm@sha256:03d12cdb63ada0401f1056fee06ace5e744399c2179b7de7d71b693a4f5c0ff8

RUN mkdir /app

WORKDIR /app
COPY requirements.txt requirements.txt
COPY requirements.dev.txt requirements.dev.txt

RUN pip install -Ur requirements.dev.txt
