<img alt="" src="https://cdn4.iconfinder.com/data/icons/social-media-and-logos-12/32/Logo_telegram_Airplane_Air_plane_paper_airplane-33-256.png" align="right" width="131"/>

# Aiogram Template

This is a template for telegram bot on aiogram3 using asynchronous database and redis<hr/>

### download

```sh
git clone git@github.com:nazar220160/AiogramTemplate.git
```

### Installation

```sh
pip install -r requirements.txt
```

#### Create db and tables. By default db is sqlite

```sh
alembic revision --autogenerate -m 'initial' && alembic upgrade head
```

#### To create locale, for example `en`:

```sh
pybabel init -i app/common/locales/messages.pot -d app/common/locales -D messages -l en
```

Extract text/update/compile:

### Unix

```sh
make babel_extract
```

```sh
make babel_update
```

```sh
make babel_compile
```

### Windows

```sh
pybabel extract --input-dirs=app -o app/common/locales/messages.pot
```

```sh
pybabel update -d app/common/locales -D messages -i app/common/locales/messages.pot
```

```sh
pybabel compile -d app/common/locales -D messages
```

## Start app:

#### for Windows:

```sh
python -m app
```

#### for Unix:

```sh
python3 -m app
```

# Docker

### Unix:

```sh
make docker_build
```

### Add migrations:

```sh
docker-compose run --rm migrate
```

```sh
make docker_up
```

## Windows:

```sh
docker-compose build && docker-compose run --rm migrate && docker-compose up -d
```

## Env file

* First of all rename your `.env_example` to `.env`

```
BOT_TOKEN=TOKEN
DATABASE_URI=postgresql+asyncpg://{}:{}@{}:{}/{}
DATABASE_NAME=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASS=postgres
ADMINS=[]
REDIS_SETTINGS={"host": "redis", "port": 6379}
```

Directory structure
-------------------

```
src/
    common/
        filters/      there is your filters
        keyboards/    there is your keyboards
        locales/      there is your locales, like en/ru
        middlewares/  there is your middlewares
        states/       there is your states
    core/
        loader.py     here is your bot configurations
        settings.py   your settings for whole app
        models.py     your models for whole app
    database/
        core/         here is your connection or main class
        dto/          here is yours data structures for database
        interfaces/   your interfaces for database
        migrations/   your db stages and versions
        models/       your db models
        repositories/ your repo for work with db models and queries
    keyboards/
        inline.py     your inline keyboards funcs
    routers/          your handlers/routers to interact with users
    services/         your business-logic
    utils/            your utils for whole app
    __main__.py       entry point
```