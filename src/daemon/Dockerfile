FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app/

COPY uv.lock .python-version pyproject.toml README.md ./
RUN uv sync

COPY src/ ./src/
COPY database/ ./database/
COPY edgedb.toml ./

ENTRYPOINT [ "uv", "run", "python3", "-m", "src.daemon" ]
