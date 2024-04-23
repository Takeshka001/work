# 1. Приветствие и ответ на команду /start: Напишите бота, который будет отвечать на 
# import os
# import dotenv
# import telebot
# from telebot import types

# dotenv.load_dotenv()

# TOKEN = os.getenv('TOKEN')
# bot = telebot.TeleBot(TOKEN)
# ADMIN_ID = os.getenv('ADMIN_ID')

# @bot.message_handler(commands=['start'])
# def start(message):
#     user_info = f'Приветствую! Этот бот поможет вам в чем-то, что вы хотите сделать.\n' \

#     bot.send_message(message.chat.id, user_info)


# if __name__ == '__main__':
#     bot.polling(non_stop=True)


# 2. Эхо-бот: Создайте бота, который будет повторять все текстовые сообщения, полученные от пользователя.

# import os
# import dotenv
# import telebot

# dotenv.load_dotenv()

# TOKEN = os.getenv('TOKEN')
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(content_types=['text'])
# def echo_message(message):
#     bot.send_message(message.chat.id, message.text)

# if __name__ == '__main__':
#     bot.polling(non_stop=True)

# 4. Калькулятор: Создайте бота, который будет принимать математические выражения от пользователя (например, "2 + 2") 
# и отправлять результат вычислений.

# import os
# import dotenv
# import telebot
# import re

# dotenv.load_dotenv()

# TOKEN = os.getenv('TOKEN')
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, "Привет! Я бот-калькулятор. Отправьте мне математическое выражение, и я постараюсь вычислить его для вас.")

# @bot.message_handler(func=lambda message: True)
# def calculate(message):
#     try:
#         expression = message.text
#         # Удаляем все символы, кроме цифр, знаков операций и пробелов
#         expression = re.sub(r'[^\d\s+\-*/().]', '', expression)
#         result = eval(expression)
#         bot.reply_to(message, f"Результат: {result}")
#     except Exception as e:
#         bot.reply_to(message, "Ошибка при вычислении. Проверьте введенное выражение и попробуйте снова.")

# if __name__ == '__main__':
#     bot.polling()


# 7.Случайные шутки: Создайте бота, который будет отправлять случайные шутки или анекдоты при запросе пользователя.
# import os
# import dotenv
# import telebot
# import requests
# from bs4 import BeautifulSoup

# dotenv.load_dotenv()

# TOKEN = os.getenv('TOKEN')
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, "Привет! Я бот со случайными шутками на русском языке. Просто отправь мне /joke, чтобы получить случайную шутку!")

# @bot.message_handler(commands=['joke'])
# def get_joke(message):
#     joke = fetch_joke()
#     if joke:
#         bot.send_message(message.chat.id, joke)
#     else:
#         bot.send_message(message.chat.id, "Извините, не удалось получить шутку. Попробуйте еще раз позже.")

# def fetch_joke():
#     url = "https://www.anekdot.ru/random/anekdot/"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             joke = soup.find("div", class_="text").get_text()
#             return joke
#     except Exception as e:
#         print("Ошибка при получении шутки:", e)
#     return None

# if __name__ == '__main__':
#     bot.polling()