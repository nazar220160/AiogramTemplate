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

### Add migrations:

```sh
docker-compose run app alembic revision --autogenerate
```

```sh
docker-compose run app alembic upgrade head
```

## Windows:

```sh
docker-compose build && docker-compose run --rm migrate && docker-compose up -d
```

## Env file

* First of all rename your `.env_example` to `.env` and `app/.env_example` to `app/.env`
