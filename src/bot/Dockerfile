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

ENTRYPOINT [ "uv", "run", "python3", "-m", "src.bot" ]
