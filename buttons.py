from telebot.types import InlineKeyboardButton as LineButton, \
    InlineKeyboardMarkup as LineMarkup, \
    ReplyKeyboardMarkup as ReplyMarkup, \
    KeyboardButton as button, ReplyKeyboardRemove as ReplyRemove

def menu(message, bot):
    '''Создание кнопок для меню'''
    markup_menu = ReplyMarkup(resize_keyboard = True)

    item_addresult = button("Добавить результат")
    item_rating = button("Рейтинг")
    item_settings = button("Настройки")
    markup_menu.add(item_addresult, item_settings, item_rating)

    bot.send_

    bot.send_message(message.chat.id, "Меню",
        reply_markup = markup_menu
    )

def rating(message, bot):
    '''Создание кнопок для выбора отображения (День, Неделя, Месяц)'''
    markup_menu = ReplyMarkup(resize_keyboard = True)

    item_day = button("День")
    item_month = button("Неделя")
    item_year = button("Месяц")

    markup_menu.add(item_day, item_month, item_year)
    bot.send_message(message.chat.id, message.text,
        reply_markup = markup_menu
    )

def settings(message, bot):
    '''создание кнопок для настроек'''
    markup_settings = ReplyMarkup(resize_keyboard = True)

    item_addresult = button("Изменить ник")
    item_cancel = button("Назад")

    markup_settings.add(item_addresult, item_cancel)
    bot.send_message(message.chat.id, message.text,
        reply_markup= markup_settings
    )

def cancel_the_operation(message, bot):
    '''создание кнопок для настроек'''
    markup_cancel = ReplyMarkup(resize_keyboard = True)

    item_cancel = button("Назад")

    markup_cancel.add(item_cancel)
    bot.send_message(message.chat.id, message.text,
        reply_markup= markup_cancel
    )

# def build_menu(buttons, n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, [header_buttons])
#     if footer_buttons:
#         menu.append([footer_buttons])
#     return menu

# def set_button_exercises(message):
#     exercises = help.exercises()
#     markup = types.InlineKeyboardMarkup()
#     for name_button in exercises:
#         button = types.InlineKeyboardButton(text=name_button, callback_data=name_button)
#         markup.add(button)
#     bot.send_message(message.chat.id, "Выбрать чат", reply_markup = markup)