from src.bot.utils.callback.models import MetaInner, _Inner, CallbackExtract


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
        com_sub = _Inner()
        remove_com_chat = _Inner()
        move_com_chats = _Inner()
        add_com_chat = _Inner()
        com_chat_toggle_turn = _Inner()
        banned_users = _Inner()
        unban = _Inner()
        move_banned_users = _Inner()
        ban = _Inner()

    class Back(metaclass=MetaInner):
        main_menu = _Inner()

    @staticmethod
    def extract(cd: str, c: bool = False, split_symbol: str = ':') -> CallbackExtract:
        args = cd.split(split_symbol)[1:] if len(cd.split(split_symbol)) > 1 else None
        cb_data = cd.split(split_symbol)[0]
        if c is True:
            cb_data = cb_data.split('~')[0]
        return CallbackExtract(data=cb_data, args=args)
