<img src="https://cdn4.iconfinder.com/data/icons/social-media-and-logos-12/32/Logo_telegram_Airplane_Air_plane_paper_airplane-33-256.png" align="right" width="131" />

# Aiogram Template

This is a template for telegram bot on aiogram3 using asynchronous database and redis<hr/>

## Setting up the .env file


```
Rename the .env-example file to .env and set your settings
```


## Local installation on Linux

```sh
# Cloning the repository
$ git clone https://github.com/nazar220160/AiogramTemplate

# Goes to the directory with the bot
$ cd AiogramTemplate

# Creating a virtual environment
$ python3 -m venv venv

# Activating the virtual environment
$ source venv/bin/activate

# Installing requirements
$ pip3 install requirements.txt

# Start bot
$ python3 -m app
```

## Installation on Docker

```bash
# Cloning the repository
git clone https://github.com/nazar220160/AiogramTemplate

# Goes to the directory with the bot
cd AiogramTemplate

# Build a docker container
docker-compose build

# Launching a docker container
docker-compose up
```
