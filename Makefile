.PHONY: install migration-generate migration-pull bot daemon lint typecheck format check

PYTHON := .venv/bin/python3

install:
	uv sync

migration-generate:
	@test -n "$(MSG)" || (echo "Error: MSG not set. Usage: make migration-generate MSG=\"Migration name\"" && exit 1)
	$(PYTHON) -m alembic revision --autogenerate -m "$(MSG)"

migration-pull:
	$(PYTHON) -m alembic upgrade head

migration-downgrade:
	@test -n "$(REV)" || (echo "Error: REV not set. Usage: make migration-downgrade REV=<revision>" && exit 1)
	$(PYTHON) -m alembic downgrade $(REV)

bot:
	$(PYTHON) -m src.bot

daemon:
	$(PYTHON) -m src.daemon

lint:
	$(PYTHON) -m ruff check src

typecheck:
	$(PYTHON) -m pyright src

format:
	$(PYTHON) -m ruff format .

check: lint typecheck format
