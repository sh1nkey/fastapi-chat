FROM python:3.11.6-slim

RUN apt-get update && apt-get -y upgrade

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.5.1

EXPOSE 8000

WORKDIR /opt/chat

COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==$POETRY_VERSION"
# https://stackoverflow.com/questions/74385209/poetry-install-throws-connection-pool-is-full-discarding-connection-pypi-org
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry install --no-interaction --no-ansi -vvv

COPY . .