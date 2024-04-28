# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/
