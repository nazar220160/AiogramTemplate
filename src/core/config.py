import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
except ImportError:
    pass

_PathLike = Union[os.PathLike[str], Path, str]


def get_env(value: str, cast_to_type: bool = False) -> Any:
    v = os.getenv(value)
    if cast_to_type and v:
        return json.loads(v)
    return v


@dataclass(frozen=True, slots=True)
class DBConfig:
    uri: str
    name: str
    host: Optional[str] = field(default=None)
    port: Optional[int] = field(default=None)
    user: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)

    @property
    def url(self) -> str:
        if "sqlite" in self.uri:
            return self.uri.format(self.name)
        return self.uri.format(
            self.user, self.password, self.host, self.port, self.name
        )


@dataclass(frozen=True, slots=True)
class BotConfig:
    token: str
    admins: List[int]


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: Optional[str] = field(default=None)
    port: Optional[int] = field(default=None)

    @property
    def dict(self) -> Optional[dict]:
        if not self.host and not self.port:
            return None

        return {"host": self.host, "port": self.port}


@dataclass(frozen=True, slots=True)
class TelegramConfig:
    api_id: int
    api_hash: str

    @property
    def params(self) -> dict:
        return {
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "system_version": "11",
            "app_version": "10.0.8 (38679)",
            "device_model": "TECNO BD4a",
            "lang_code": "ru",
            "system_lang_code": "ru-RU",
        }


@dataclass(frozen=True, slots=True)
class Config:
    db: DBConfig
    bot: BotConfig
    redis: RedisConfig
    telegram: TelegramConfig

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @classmethod
    def path(cls, *paths: _PathLike, base_path: Optional[_PathLike] = None) -> str:
        if base_path is None:
            base_path = cls.root_dir()

        return os.path.join(base_path, *paths)


def load_config() -> Config:
    return Config(
        db=DBConfig(
            uri=get_env("DB_URI"),
            name=get_env("DB_NAME"),
            host=get_env("DB_HOST"),
            port=get_env("DB_PORT", True),
            user=get_env("DB_USER"),
            password=get_env("DB_PASSWORD"),
        ),
        bot=BotConfig(token=get_env("BOT_TOKEN"), admins=get_env("BOT_ADMINS", True)),
        redis=RedisConfig(
            host=get_env("REDIS_HOST"),
            port=get_env("REDIS_PORT"),
        ),
        telegram=TelegramConfig(
            api_id=get_env("TELEGRAM_API_ID"), api_hash=get_env("TELEGRAM_API_HASH")
        ),
    )
