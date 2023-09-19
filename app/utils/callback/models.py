from typing import Optional
from pydantic import BaseModel


class CallbackExtract(BaseModel):
    data: str
    args: Optional[list]


class AutoClassName(type):
    def __str__(self):
        return self.__name__


class MetaInner(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, _Inner):
                attr_value.name = f"{name}~{attr_name}"
        return super().__new__(mcs, name, bases, attrs)

    def __call__(cls, *args):
        if not args:
            return cls.__name__
        else:
            return super().__call__(*args)


class _Inner:
    def __init__(self):
        self.name = None

    def __call__(self, *args):
        if not args:
            return self.name
        args = map(str, args)  # Convert all elements in args to strings
        return f"{self.name}~{'~'.join(args)}"
