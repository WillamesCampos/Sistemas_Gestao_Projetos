FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install poetry
RUN poetry install

COPY . .
