import telebot
import datetime
import math
from telebot import types
import threading
bot = telebot.TeleBot('токен')

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Дата', 'Мем')
    markup.row('Калькулятор','Заметки')
    bot.send_message(message.chat.id, 'Привет! Что ты хочешь сделать?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Дата')
def date(message):
    bot.send_message(message.chat.id, f'Сегодня {datetime.date.today().strftime("%d.%m.%Y")}')


@bot.message_handler(content_types=['text', 'photo', 'sticker'])
def handle_message(message):
 
  if message.text == 'Привет':
      bot.send_message(message.chat.id, 'Привет! Как дела?')
  elif message.text == 'Нормально':
      bot.send_message(message.chat.id, 'Понял,у меня все норм.')
  elif message.text == 'Хорошо':
      bot.send_message(message.chat.id, 'Понял,у меня все норм.')
  elif message.text == 'Плохо':
      bot.send_message(message.chat.id, 'Кто грустит,того рот кхм...')
  elif message.sticker:
      bot.send_message(message.chat.id, 'Не люблю стикеры')
  elif message.text == 'Я скучаю':
      bot.send_photo(message.chat.id, open('123.jpg', 'rb'))
  elif message.text == 'Мем':
      bot.send_photo(message.chat.id, open('qwe.png', 'rb'))
  elif message.text == 'Калькулятор':
      bot.send_message(message.chat.id, 'Введи выражение для вычисления')
      bot.register_next_step_handler(message, calc)
  elif message.text == 'Заметки':
    bot.send_message(message.chat.id, "О чём напомнить?")
    bot.register_next_step_handler(message, set_note_name)
  else:
      bot.send_message(message.chat.id, 'Я тебя не понял.')

def set_note_name(message):
    user_data = {}
    user_data[message.chat.id] = {'note_name': message.text}
    bot.send_message(message.chat.id, 'Когда напомнить? ГГГГ-ММ-ДД чч:мм:сс.')

    bot.register_next_step_handler(message, set_note_date, user_data)

def set_note_date(message, user_data):
    try:
        note_date = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delta = note_date - now
        if delta.total_seconds() <= 0:
            bot.send_message(message.chat.id, 'эта дата в прошлом...')
            
        else:
            note_name = user_data[message.chat.id]['note_name']
            bot.send_message(message.chat.id, 'Напомню "{}" в {}.'.format(note_name, note_date))
            
            note_date = threading.Timer(delta.total_seconds(), notify, [message.chat.id, note_name])
            note_date.start()
   
    except:
        bot.send_message(message.chat.id, 'не то')



def notify(chat_id, note_name):
    bot.send_message(chat_id, 'Напоминание: "{}"!'.format(note_name))


def calc(message):
    try:
        result = eval(message.text)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except Exception as e:
        bot.send_message(message.chat.id, 'Неверное выражение')

bot.polling()