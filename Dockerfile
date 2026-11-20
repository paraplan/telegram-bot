FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS base
WORKDIR /app
ENV TZ="Europe/Moscow"
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY uv.lock .python-version pyproject.toml README.md ./

FROM base AS dependencies
RUN uv sync --locked --no-dev --no-install-project
COPY src/ ./src/
RUN uv sync --locked --no-dev --no-editable

FROM base AS runtime
COPY --from=dependencies /app/.venv /app/.venv
COPY alembic.ini ./
COPY migrations/ ./migrations/

