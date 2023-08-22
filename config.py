import json
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
CREATE_ENGINE: str = env.str("CREATE_ENGINE")
DEBUG: bool = env.bool("DEBUG")

sub_list = json.load(open('data/sub_list.json', 'r', encoding='utf-8'))
bot_commands = json.load(open('data/bot_commands.json', 'r', encoding='utf-8'))
