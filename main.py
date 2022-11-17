# from telebot import TeleBot
# from config import TOKEN
# from helper import firstMSG
# from db.database import user_exists, db_conn, user_auth

# print('Пошла жара!!!')
# #bot
# bot = TeleBot(TOKEN)
# print('Бот готов к работе')

# # print('Подключение к бд. Запуск')
# # db_conn()
# # print('Подключение к бд. Запуск прошёл успешно')
# db_conn()


# @bot.message_handler(commands=['start'])
# def get_start(message):
#     sti = open('static/welcome.webp', 'rb')
#     user_exists(message.chat.id)
#     # user_auth(message.chat.id)
#     msg = firstMSG(message.chat.id)
    
#     bot.send_message(message.chat.id, (msg + message.from_user.first_name + message.from_user.last_name))
#     bot.send_photo(message.chat.id, sti)


# @bot.message_handler(commands=['add_result'])
# def add_result(message):
#     msgText =  'Ну давай запишем \n\nСколько раз сделал?'
#     msg = bot.send_message(message.chat.id, msgText)    
#     bot.register_next_step_handler(msg, set_num_approaches)


# def set_num_approaches(message):
#     if int(message.text) > 20:
#         msgText = 'Ништяк!!! '
#     else:
#         msgText = 'Окей '
    
#     msgText += 'А теперь количество подходов'


#     msg = bot.send_message(message.chat.id, 'Я записал твои результаты на текущую дату, до следующего раза, Мужчина!')  

# print('Бот запущен')

# bot.polling(none_stop=True)


from urllib import response
from telebot import TeleBot, types
from config import TOKEN, msgs
import helper as help

print('Пошла жара!!!')
#bot
bot = TeleBot(TOKEN)
print('Бот готов к работе')

@bot.message_handler(commands=['start'])
def get_start(message):
    msg = help.user_verification(message.chat.id)
    if msg == msgs['registr']:
        msg = bot.send_message(message.chat.id, msg)    
        bot.register_next_step_handler(msg, register)
    else:
        welcome(message, msg)

#обработка нажатых кнопок
@bot.message_handler(content_types=['text'])
def use_menu(message):
    if message.text == 'Добавить результат':
        get_exercise(message)
    if message.text == 'Настройки':
        use_settings(message)

def register(message):
    print(message.text)
    msg = help.user_register(message.chat.id, message.text)
    welcome(message, msg)

def welcome(message, msg):
    bot.send_message(message.chat.id, (message.from_user.full_name + ', ' + msg))

    image = open('static/welcome.webp', 'rb')
    bot.send_photo(message.chat.id, image)
    menu(message)

#создание кнопок для управления меню
def menu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item_addresult = types.KeyboardButton('Добавить результат')
    item_settings = types.KeyboardButton('Настройки')

    markup_menu.add(item_addresult, item_settings)
    bot.send_message(message.chat.id, 'Меню',
        reply_markup = markup_menu
    )

#создание кнопок для настроек
def use_settings(message):
    bot.send_message(message.chat.id, "Настройки", reply_markup=types.ReplyKeyboardRemove())
        
    markup_settings = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item_addresult = types.KeyboardButton('Изменить ник')
    item_settings = types.KeyboardButton('Назад')

    markup_settings.add(item_addresult, item_settings)
    bot.send_message(message.chat.id, 'Меню',
        reply_markup = markup_settings
    )

def get_exercise(message):
    bot.send_message(message.chat.id, "Добавить результат", reply_markup=types.ReplyKeyboardRemove())
    
    msgText =  'Ну давай запишем \nСколько раз сделал?'
    msg = bot.send_message(message.chat.id, msgText)    
    bot.register_next_step_handler(msg, get_approaches)

def get_approaches(message):
    if int(message.text) > 20:
        msgText = 'Ништяк!!! '
    else:
        msgText = 'Окей '
    msg = bot.send_message(message.chat.id, msgText)

    msgText = 'А теперь количество подходов:'
    msg = bot.send_message(message.chat.id, msgText)
    bot.register_next_step_handler(msg, set_result)

def set_result(message):
    msgText = 'Я записал твои результаты на текущую дату, до следующего раза, Мужчина!'

    bot.send_message(message.chat.id, msgText)  
    menu(message)

print('Бот запущен')

bot.polling(none_stop=True)