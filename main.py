#from urllib import response
from telebot import TeleBot, types

import buttons
import re
import db.helper as help
from config import TOKEN, msgs

#Константы
update_name = "Ваш ник изменен"

print("Запуск бота")
bot = TeleBot(TOKEN)

print("Подключение установлено")

@bot.message_handler(commands=["start"])
def get_start(message):
    '''Запуск бота клиентом'''
    msg = help.user_verification(message.chat.id)
    help.exercises()

    if msg == msgs["registr"]:
        msg = bot.send_message(message.chat.id, msg)    
        bot.register_next_step_handler(msg, register)
    else:
        user_name = help.user_name(message.chat.id)
        welcome(message, msg, user_name)

@bot.message_handler(content_types=["text"])
def use_menu(message):
    '''Обработка нажатых кнопок'''
    if message.text == "Добавить результат":
        buttons.cancel_the_operation(message, bot)
        get_exercise(message)

    if message.text == "Настройки":
        buttons.settings(message, bot)

    if message.text == "Назад":
        buttons.menu(message, bot)
    
    if message.text == "Рейтинг":
        buttons.rating(message, bot)

    if message.text == "Изменить ник":
        msgText =  "Введите желаемое имя"
        buttons.cancel_the_operation(message, bot)
        msg = bot.send_message(message.chat.id, msgText)  
        bot.register_next_step_handler(msg, update_user_name)

def update_user_name(message): 
    '''Изменение имени пользователя'''
    if message.text != "Назад":
        help.update_user_name(message.chat.id, message.text)
        welcome(message, update_name, message.text)
    else:
        use_menu(message)

def register(message):
    '''Регистрация нового пользователя'''
    msg = help.user_register(message.chat.id, message.text)
    welcome(message, msg, message.text)

def welcome(message, msg, user_name):
    '''Приветствие пользователя'''
    bot.send_message(message.chat.id, (user_name + ', ' + msg))

    if msg != update_name:
        image = open("static/welcome.webp", "rb")
        bot.send_photo(message.chat.id, image)

    buttons.menu(message, bot)

def get_exercise(message):
    '''Внесение результата пользователя'''
    msgText =  "Ну давай запишем \nСколько раз сделал?"
    msg = bot.send_message(message.chat.id, msgText)  
    bot.register_next_step_handler(msg, get_approaches)

def get_approaches(message):
    '''Обработка внесеного пользователем результата'''
    if bool(re.match("^[0-9 ]", message.text)): 

        if int(message.text) > 20:
            msgText = "Ништяк!!!"
        else:
            msgText = "Окей"
        msg = bot.send_message(message.chat.id, msgText)

        msgText = "А теперь количество подходов:"
        msg = bot.send_message(message.chat.id, msgText)
        bot.register_next_step_handler(msg, set_result)
    else:
        use_menu(message)

def set_result(message):
    '''Сохранение результата'''
    msgText = "Я записал твои результаты на текущую дату, до следующего раза, Мужчина!"

    bot.send_message(message.chat.id, msgText)  
    buttons.menu(message)

print("Бот запущен")

bot.polling(none_stop=True)