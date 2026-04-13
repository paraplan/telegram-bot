# Paraplan

The most convenient way for students of the Vitebsk State College of Electrical Engineering to get their class schedule.

This project is written in Python and is a modern Telegram bot built with [telegrinder](https://github.com/timoniq/telegrinder). PostgreSQL is used as the database.

## Deployment

1. Clone this repo anywhere
2. Create the .env file from the example:
```shell
cp .env{.example,}
```
3. Run `docker compose up --build -d`

## Development

We strongly recommend using the [Nix](https://nixos.org/download/) package manager for development. Nix will install all the necessary dependencies for you, ensuring you have the same Python version as other contributors.

> [!NOTE]
> However, you can also get by with a locally installed [uv](https://docs.astral.sh/uv/#installation) package manager, but in that case, be prepared to troubleshoot issues manually :)

Steps to set up the development environment:

1. Run `nix develop`
2. Run `make` to install Python dependencies
3. Set up a PostgreSQL database and create the .env file from the example: `cp .env{.example,}`
4. Check out the `Makefile` for available commands
