FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS system

ENV TZ="Europe/Moscow"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales git \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


FROM system AS builder

WORKDIR /app

COPY uv.lock .python-version pyproject.toml ./

RUN uv sync --frozen


FROM builder AS runtime

COPY --from=builder /app /app

COPY src/ ./src/

ENTRYPOINT [ "uv", "run", "python3", "-m", "src.daemon" ]
