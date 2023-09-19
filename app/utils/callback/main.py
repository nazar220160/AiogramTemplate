from app.utils.callback.models import MetaInner, _Inner, CallbackExtract


class CallbackData:
    class Start(metaclass=MetaInner):
        ...

    class Admin(metaclass=MetaInner):
        ross = _Inner()
        get_admins = _Inner()
        remove_admin = _Inner()
        move_admins = _Inner()
        main = _Inner()
        confirm_ross = _Inner()

    class Back(metaclass=MetaInner):
        main_manu = _Inner()

    @staticmethod
    def extract(data: str, c: bool = False) -> CallbackExtract:
        _data = "~".join(data.split("~")[:2])
        args = data.split("~")[2:] if len(data.split("~")) > 2 else None
        if c is True:
            return CallbackExtract(data=data.split("~")[0], args=args)
        return CallbackExtract(data=_data, args=args)
