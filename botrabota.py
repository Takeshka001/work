import os
import csv
import dotenv
import telebot
import datetime
from telebot import types
from geopy.geocoders import Nominatim

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = os.getenv('ADMIN_ID')

# Глобальная переменная для хранения статуса
status = ''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Пришел')
    btn2 = types.KeyboardButton('Ушел')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Укажите статус?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Пришел')
def ask_for_arrival_location(message):
    global status
    status = 'Пришел'
    request_location(message)

@bot.message_handler(func=lambda message: message.text == 'Ушел')
def ask_for_departure_location(message):
    global status
    status = 'Ушел'
    request_location(message)

def request_location(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    btn = types.KeyboardButton('Отправить местоположение', request_location=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)
    bot.send_message(message.chat.id, 'Пожалуйста, отправьте свое местоположение.', reply_markup=markup)



@bot.message_handler(content_types=['location'])
def save_location(message):
    global status
    
    with open('location.csv', 'a', newline='') as file:
        date = datetime.datetime.now()
        date_str = date.strftime("%d.%m.%Y %H:%M:%S")  # Форматирование даты и времени
        writer = csv.writer(file)
        writer.writerow([
            message.chat.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.location.latitude if message.location else '',
            message.location.longitude if message.location else '',
            status,
            date_str,  # Используем отформатированную дату и время
        ])
    bot.send_message(message.chat.id, f'Вы отмечены как {"пришедший" if status == "Пришел" else "ушедший"}')

    # После отправки местоположения показываем главные кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Пришел')
    btn2 = types.KeyboardButton('Ушел')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
 
if __name__ == '__main__':
    bot.polling(non_stop=True)