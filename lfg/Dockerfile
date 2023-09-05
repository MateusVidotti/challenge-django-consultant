FROM python:3.11.4-slim
WORKDIR /code

# variáveis para desenvolvimento
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH /code

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

# Instala apenas as dependências.
COPY ./lfg .
#COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

COPY ./lfg/start-celeryworker /start-celeryworker
RUN chmod +x /start-celeryworker
COPY ./lfg/start-django /start-django
RUN sed -i 's/\r$//g' /start-django
RUN chmod +x /start-django
