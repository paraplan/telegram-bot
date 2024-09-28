FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV TZ="Europe/Moscow"

WORKDIR /app

COPY uv.lock .python-version pyproject.toml README.md ./
RUN uv sync

COPY src/ ./src/

ENTRYPOINT [ "uv", "run", "python3", "-m", "src.daemon" ]
