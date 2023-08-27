from dataclasses import dataclass


@dataclass
class BotCommands:
    command: str
    description: str


@dataclass
class CallbackExtract:
    data: str
    args: list
