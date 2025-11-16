FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

FROM base AS dev

ENV APP_ENV=development

COPY spectragraph-core /app/spectragraph-core
COPY spectragraph-types /app/spectragraph-types
COPY spectragraph-transforms /app/spectragraph-transforms

COPY spectragraph-api /app/spectragraph-api

WORKDIR /app/spectragraph-api

RUN poetry install --no-root

EXPOSE 5001

ENTRYPOINT ["/app/spectragraph-api/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]

# Production stage
FROM base AS prod

ENV APP_ENV=production

COPY spectragraph-core /app/spectragraph-core
COPY spectragraph-types /app/spectragraph-types
COPY spectragraph-transforms /app/spectragraph-transforms

COPY spectragraph-api /app/spectragraph-api

WORKDIR /app/spectragraph-api

RUN poetry install

EXPOSE 5001

ENTRYPOINT ["/app/spectragraph-api/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
