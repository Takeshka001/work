import csv
from datetime import datetime
from telebot import TeleBot, types
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

bot = TeleBot("6982924871:AAG0s-Sr9ZK8SUA8SAjeg5YvHQd21Q2Piak", parse_mode="HTML")


def default_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    k1 = types.KeyboardButton("Пришел")
    k2 = types.KeyboardButton("Ушел")
    markup.row(k1)
    markup.row(k2)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    u_id = message.chat.id
    bot.send_message(u_id, "Привет ты пришел или ушел", reply_markup=default_keyboard())


@bot.message_handler(func=lambda message: message.text == "Отмена")
def cancel(message):
    u_id = message.chat.id
    bot.send_message(u_id, "Привет ты пришел или ушел", reply_markup=default_keyboard())


def get_location_keyboard():
    location_button = types.KeyboardButton("Отправить местоположение", request_location=True)
    return types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(location_button)


def has_come_next(bot: TeleBot, message: types.Message, otchet: str):
    user = message.from_user
    location_address = "Неизвестное местоположение"

    if not message.location:
        bot.send_message(
            chat_id=user.id,
            text="Пожалуйста, отправьте свое местоположение.",
            reply_markup=get_location_keyboard()
        )
        return

    try:
        longitude = message.location.longitude
        latitude = message.location.latitude
        geolocator = Nominatim(user_agent="Telegram_Bot")
        location = geolocator.reverse((latitude, longitude))
        location_address = location.address if location else "Неизвестное местоположение"
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        bot.send_message(
            chat_id=user.id,
            text="Ошибка при получении местоположения. Пожалуйста, попробуйте позже."
        )
        return
    
    user_data = [
        user.id,
        user.first_name or "Неизвестно",
        user.last_name or "Неизвестно",
        otchet,
        datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        location_address
    ]
    
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(user_data)
    
    bot.send_message(
        chat_id=user.id,
        text=f"Отчет:\n{' | '.join(map(str, user_data))}\nУдачи в работе, {user.first_name}!",
        reply_markup=default_keyboard()
    )


def has_come_next(message, otchet):
    user: types.User = message.from_user
    try:
        longitude = message.location.longitude
        latitude = message.location.latitude
        location = Nominatim(user_agent="Telegram").reverse(f"{latitude}, {longitude}")
    except AttributeError:
        bot.send_message(user.id, "Отправьте местоположение", reply_markup=get_location_keyboard())
        bot.register_next_step_handler(message, has_come_next, otchet)


    dd = [user.id, user.first_name, user.last_name, otchet, datetime.now().strftime("%d.%m.%Y %H:%M:%S"), f"<code>{location.address}</code>"]

    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        dd.pop()
        writer.writerow(dd+ [location.address])
    bot.send_message(user.id, "\n".join(map(str, dd+[location.address])) + f"\nУдачи на работе {user.first_name}", reply_markup=default_keyboard())


@bot.message_handler(func=lambda message: message.text.lower() in ["пришел", "ушел"])
def has_come(message):
    u_id = message.chat.id

    bot.send_message(u_id, "Отправьте мне свае местоположение", reply_markup=get_location_keyboard())
    bot.register_next_step_handler(message, has_come_next, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)