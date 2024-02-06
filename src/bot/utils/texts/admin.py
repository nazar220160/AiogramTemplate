from src.bot.common.middlewares.i18n import gettext as _

START = _("<b>Всего пользователей</b> - {len_users}\n\n"
          "<b>Добавить админа</b> - <code>/add_admin user_id</code>")

ADD_COM_CHAT = _("<b>Обязательная подписка</b>: <i>Добавление чата</i>\n\n"
                 "<i>Добавьте бота в администраторы канала используя кнопки</i>")

GET_COM_CHAT_NOT_ADMIN = _("Чтобы добавить канал в ОП бот должен быть администратором канала!")
GET_COM_CHAT_ALREADY_IN_DB = _("Этот чат уже есть в обязательной подписке!")
GET_COM_CHAT_MUST_BE_PUBLIC = _("Чат обязательно должен быть публичный")

UNKNOWN_ERROR = _("Неизвестная ошибка!")
MESSAGE_MUST_BE_FORWARD_FROM_CHANNEL = _("Сообщение должно быть переслано из канала!")
MUST_BE_INTEGER = _("ID чата должен состоять только из цифр!")

REPLY_SEND = _("Ответ отправлен!")
ERROR = _("Ошибка!")

USER_BLOCKED_BOT_OR_DELETE_MESSAGE = _("Пользователь удалил сообщение либо заблокировал бота!")
MESSAGE_ALREADY_ANSWERED = _("Сообщение уже отвечено!")
MESSAGE_NOT_FOUND = _("Не найдено сообщение для ответа!")

SUCCESSFUL = _("Успешно")
FOR_SEND_MESSAGE_ENTER_COMMAND = _("Для отправки монет пользователя введите команду:\n"
                                   "/send_money ID сумма")

ROSS_DONE = _("<b>Завершено. Успешно: {good}. Неудач: {errors}</b>")
ROSS_FILE_NAME = _("Рассылка сообщений {date}.txt")
INSUFFICIENT_PERMISSIONS = _("Недостаточно прав!")
ADMIN_PANEL_COM_SUB = _("<b>Админ панель</b>: <i>Обязательная подписка</i>")
ENTER_MESSAGE_FOR_ROSS = _("<b>Отправьте сообщение для рассылки</b>")
BANNED_USERS = _("<b>Админ панель</b>: <i>Заблокированные пользователи</i>\n\n"
                 "<i>Список заблокированных пользователей</i>")
SEND_USER_ID_TO_BAN = _("<b>Админ панель</b>: <i>Блокировка пользователя</i>\n\n"
                        "<i>Отправьте ID пользователя которого хотите заблокировать</i>")
USER_NOT_FOUND = _("<b>Ошибка</b>: <i>Пользователь не существует</i>")
BAN_USER_SUCCESSFUL = _("<b>Админ панель</b>: <i>Блокировка пользователя</i>\n\n"
                        "<i>Пользователь {} успешно заблокирован!</i>")
