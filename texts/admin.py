def start(len_users) -> str:
    return f"<b>Всего пользователей</b> - {len_users}\n\n" \
           f"<b>Отправка монет</b> - <code>/send_money user_id сумма</code>\n" \
           f"<b>Добавить админа</b> - <code>/add_admin user_id</code>"
