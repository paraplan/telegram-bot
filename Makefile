.PHONY: install migration-generate migration-pull migration-downgrade bot daemon lint typecheck format check

install:
	uv sync

migration-generate:
	@test -n "$(MSG)" || (echo "Error: MSG not set. Usage: make migration-generate MSG=\"Migration name\"" && exit 1)
	uv run alembic revision --autogenerate -m "$(MSG)"

migration-pull:
	uv run alembic upgrade head

migration-downgrade:
	@test -n "$(REV)" || (echo "Error: REV not set. Usage: make migration-downgrade REV=<revision>" && exit 1)
	uv run alembic downgrade $(REV)

bot:
	uv run paraplan

daemon:
	uv run daemon

lint:
	uv run ruff check src

typecheck:
	uv run basedpyright src

format:
	uv run ruff format .

check: lint typecheck
	uv run ruff format --check .
