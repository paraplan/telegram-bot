# Телеграмм бот для расписания

## Как запустить локально?

1. Установить все зависимости

-   [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
-   [Edgedb](https://docs.edgedb.com/get-started/quickstart#installation)

2. Установить пакеты и инициализировать базу данных

```zsh
poetry install --with dev
edgedb project init
```

3. Запустить пакет

```zsh
poetry run python3 -m bot # либо daemon, schedule_parser
```
