from telebot.types import InlineKeyboardButton as LineButton, \
    InlineKeyboardMarkup as LineMarkup, \
    ReplyKeyboardMarkup as ReplyMarkup, \
    KeyboardButton as button, ReplyKeyboardRemove as ReplyRemove
import db.helper as help

def menu(message, bot):
    '''Создание кнопок для меню'''
    markup_menu = ReplyMarkup(resize_keyboard = True)

    item_addresult = button("Добавить результат")
    item_rating = button("Рейтинг")
    item_settings = button("Настройки")
    markup_menu.add(item_addresult, item_settings, item_rating)

    #bot.send_

    bot.send_message(message.chat.id, "Меню",
        reply_markup = markup_menu
    )

def rating(message, bot):
    '''Создание кнопок для выбора отображения (День, Неделя, Месяц)'''
    markup_menu = ReplyMarkup(resize_keyboard = True)

    item_day = button("День")
    item_month = button("Неделя")
    item_year = button("Месяц")
    item_cancel = button("Назад")

    markup_menu.add(item_day, item_month, item_year)
    markup_menu.add(item_cancel)
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

def set_button_exercises(message, bot):
    '''Генерация кнопок исходя из колличества упражнений'''
    msg = "Выберете упражнение"
    exercises = help.exercises()
    markup = LineMarkup()
    for name_button in exercises:
        button = LineButton(text=name_button, callback_data=name_button)
        markup.add(button)
    bot.send_message(message.chat.id, msg, reply_markup = markup)
    return exercises