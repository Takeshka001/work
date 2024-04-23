import os
import dotenv
import telebot
import datetime
from telebot import types

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = os.getenv('ADMIN_ID')

@bot.message_handler(commands=['start'])
def start(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f'Информация о пользователе:\n\n' \
                f'ID чата: {message.chat.id}\n' \
                f'ID пользователя: {message.from_user.id}\n' \
                f'Имя: {message.from_user.first_name}\n' \
                f'Фамилия: {message.from_user.last_name}\n' \
                f'Псевдоним: {message.from_user.username}\n' \
                f'Текст сообщения: {message.text}\n' \
                f'Время нажатия кнопки "Старт": {current_time}\n'
    
    bot.send_message(message.chat.id, user_info)

    # Отправляем запрос на отправку местоположения
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваше местоположение на карте.")

@bot.message_handler(commands=['help'])
def help(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Связаться с Оператором', request_contact=True)
    btn2 = types.KeyboardButton('FAQ')
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, 'Выберете действие!', reply_markup=markup)
    bot.send_message(message.chat.id, 'Выберете действие!')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "Связаться с Оператором":
        bot.send_message(message.chat.id, "Оператор свяжется с Вами в ближайшее время!")
    elif message.text == "FAQ":
        bot.send_message(message.chat.id, "Оператор свяжется с Вами в ближайшее время!")

@bot.message_handler(content_types=['contact'])
def contact(message):
    bot.send_message(ADMIN_ID, f"Новая заявка:\n\n"
                                f"ID чата: {message.chat.id}\n"
                                f"ID пользователя: {message.from_user.id}\n"
                                f"Имя: {message.from_user.first_name}\n"
                                f"Фамилия: {message.from_user.last_name}\n"
                                f"Псевдоним: {message.from_user.username}\n"
                                f"Телефон: {message.contact.phone_number}\n")
    bot.send_message(message.chat.id, "Оператор свяжется с Вами в ближайшее время!")



if __name__ == '__main__':
    bot.polling(non_stop=True)



    