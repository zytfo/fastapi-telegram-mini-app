FROM python:3.11-slim

RUN pip install fastapi uvicorn poetry wheel virtualenv

EXPOSE 8000

WORKDIR /usr/src/api

COPY . /api/src
COPY ./main.py /api
COPY ./pyproject.toml /api

WORKDIR /api
RUN poetry config virtualenvs.create false \
  && poetry install

COPY . ./