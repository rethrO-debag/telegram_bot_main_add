from urllib import response
from telebot import TeleBot, types
from config import TOKEN
import helper

print('Пошла жара!!!')
#bot
bot = TeleBot(TOKEN)
print('Бот готов к работе')

@bot.message_handler(commands=['start'])
def get_start(message):
    msg = helper.firstMSG(message.chat.id)
    
    bot.send_message(message.chat.id, (message.from_user.full_name + ', ' + msg))

    sti = open('static/welcome.webp', 'rb')
    bot.send_photo(message.chat.id, sti)
    add_button(message)

def add_button(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item_id = types.KeyboardButton('Добавить результат')

    markup_reply.add(item_id)
    bot.send_message(message.chat.id, 'Меню',
        reply_markup = markup_reply
    )

@bot.message_handler(content_types=['text'])
def get_exercise(message):
    if message.text == 'Добавить результат':
        bot.send_message(message.chat.id, "Добавить результат", reply_markup=types.ReplyKeyboardRemove())
        msgText =  'Ну давай запишем \n\nСколько раз сделал?'
        #data = helper.exercises_button()
        #for data in results:

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

    msg = bot.send_message(message.chat.id, msgText)  
    add_button(message)

print('Бот запущен')

bot.polling(none_stop=True)