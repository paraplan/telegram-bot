# Телеграмм бот для расписания

## Как запустить локально?

1. Установить все зависимости

-   [uv](https://docs.astral.sh/uv)
-   [Edgedb](https://docs.edgedb.com/get-started/quickstart#installation)

2. Установить пакеты и инициализировать базу данных

```zsh
uv sync
edgedb project init
```

3. Запустить нужный модуль

```zsh
uv run python3 -m src.bot # либо src.daemon, src.schedule_parser
```
