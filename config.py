import json
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
DB_USERNAME: str = env.str("DB_USERNAME")
DB_PASS: str = env.str("DB_PASS")
DB_HOST: str = env.str("DB_HOST")
DB_PORT: str = env.str("DB_PORT")
DB_NAME: str = env.str("DB_NAME")

db_url = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sub_list = json.load(open('telegram_bot/data/sub_list.json', 'r', encoding='utf-8'))
bot_commands = json.load(open('telegram_bot/data/bot_commands.json', 'r', encoding='utf-8'))
