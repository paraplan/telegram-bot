# Параплан - расписание занятий для студентов Витебского государственного колледжа электротехники.

## Как запустить сервер?

```zsh
cp .env.example .env
vim .env
docker compose up -d
```

## Как запустить локально?

1. Установить все зависимости

-   [postgresql](https://www.postgresql.org/download/)
-   [uv](https://docs.astral.sh/uv)

2. Установить пакеты и сделать миграции

```zsh
uv sync
uv run alembic upgrade head
```

3. Скопировать и изменить .env

```zsh
cp .env.example .env
vim .env
```

4. Запустить нужный модуль

```zsh
uv run python -m src.bot # либо src.daemon, src.schedule_parser
```
