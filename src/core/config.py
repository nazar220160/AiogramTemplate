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

    webhook_host: Optional[str] = field(default=None)
    webhook_port: Optional[int] = field(default=None)
    webhook_url: Optional[str] = field(default=None)
    webhook_path: Optional[str] = field(default=None)
    webhook_secret: Optional[str] = field(default=None)
    
    @property
    def use_webhook(self) -> bool:
        return (
            self.webhook_host is not None
            and self.webhook_port is not None
            and self.webhook_url is not None
            and self.webhook_path is not None
        )


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: Optional[str] = field(default=None)
    port: Optional[int] = field(default=None)
    db: Optional[int] = field(default=None)

    @property
    def dict(self) -> Optional[dict]:
        if not self.host and not self.port:
            return None

        return {"host": self.host, "port": self.port, "db": self.db}


@dataclass(frozen=True, slots=True)
class Config:
    db: DBConfig
    bot: BotConfig
    redis: RedisConfig

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
        bot=BotConfig(
            token=get_env("BOT_TOKEN"),
            admins=get_env("BOT_ADMINS", True),
            webhook_host=get_env("BOT_WEBHOOK_HOST"),
            webhook_port=get_env("BOT_WEBHOOK_PORT", True),
            webhook_url=get_env("BOT_WEBHOOK_URL"),
            webhook_path=get_env("BOT_WEBHOOK_PATH"),
            webhook_secret=get_env("BOT_WEBHOOK_SECRET"),
        ),
        redis=RedisConfig(
            host=get_env("REDIS_HOST"),
            port=get_env("REDIS_PORT"),
            db=get_env("REDIS_DB", True),
        ),
    )
