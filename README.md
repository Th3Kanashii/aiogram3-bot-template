# aiogram3-bot-template

This template uses code from a [repository](https://github.com/wakaree/aiogram_bot_template) that is licensed under the MIT License. I am grateful to the [wakaree](https://github.com/wakaree) for creating and publishing this code.

The original license of the borrowed code can be found in the [COPYING file](COPYING).

## System dependencies

- Python 3.8+
- Docker
- docker-compose
- make
- hatch

## Deployment

### Via [Docker](https://www.docker.com/)

- Rename `.env.dist` to `.env` and configure it
- Configure `docker-compose.yml`
- Run `make app-build` command then `make app-run` to start the bot

### Via Systemd service

- Configure and start [PostgreSQL](https://www.postgresql.org/)
- Rename `.env.dist` to `.env` and configure it
- Configure url in `alembic.ini`
- Run database migrations with `make migrate` command
- Configure `systemd/telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

## Development

### Setup environment

    make dev

### Update database tables structure

**Make migration script:**

    make migration name=NAME_MIGRATION --rev-id=ID_MIGRATION

**Run migrations:**

    make migrate

## Used technologies

- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
