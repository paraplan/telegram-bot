FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS base
WORKDIR /app
ENV TZ="Europe/Moscow"
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY uv.lock .python-version pyproject.toml ./

FROM base AS dependencies
RUN uv sync --frozen --no-dev

FROM base AS runtime
COPY --from=dependencies /app/.venv /app/.venv
COPY templates/ ./templates/
COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/

