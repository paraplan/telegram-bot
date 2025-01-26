FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV TZ="Europe/Moscow"
# Set the locale
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

WORKDIR /app/

COPY uv.lock .python-version pyproject.toml README.md ./
RUN uv sync

COPY templates/ ./templates/
COPY src/ ./src/

COPY alembic.ini ./
COPY migrations/ ./migrations/

RUN chmod +x /app/src/bot/docker-entrypoint.sh

ENTRYPOINT [ "/app/src/bot/docker-entrypoint.sh" ]
