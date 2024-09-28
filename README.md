# Параплан - расписание ВГКЭ

## Как запустить сервер?

```zsh
cp .env.example .env
vim .env
docker compose up -d
```


## Как запустить локально?

1. Установить все зависимости

-   [uv](https://docs.astral.sh/uv)
-   [Edgedb](https://docs.edgedb.com/get-started/quickstart#installation)

2. Установить пакеты и инициализировать базу данных

```zsh
uv sync
edgedb project init
```

3. Скопировать и изменить .env
```zsh
cp .env.example .env
vim .env
```

4. Запустить нужный модуль

```zsh
uv run python3 -m src.bot # либо src.daemon, src.schedule_parser
```
