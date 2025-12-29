#!/bin/sh

uv run alembic upgrade head
uv run python3 -m src.bot
