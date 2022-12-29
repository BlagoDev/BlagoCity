"""
Модуль для команды /start

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""

# Импорт библиотек
# Встроенные библиотеки
from os import getenv                               # Получение доступа к .env переменным
# Сторонние библиотеки
from dotenv import load_dotenv                      # Выгрузка данных из .env переменных
from telebot import TeleBot                         # Класс бота в Telegram
from telebot.types import Message, \
    ReplyKeyboardMarkup, KeyboardButton             # Типы данных для грамотного использования Telegram


# Выгружаем файл с кнопками и сообщениями
load_dotenv(r'StaffFiles\message_text.env')

# Для редактирования текста кнопок и сообщений
# откройте файл message_text.env в папке StaffFiles и измените интересующую
# вас переменную!
# (Естественно, на Github'е этой папки не будет)

# Кнопки
button_2: str = getenv('BUTTON_2')
button_3: str = getenv('BUTTON_3')

# Сообщения
message_2: str = getenv('MESSAGE_2')
message_3: str = getenv('MESSAGE_3')


def start(bot: TeleBot, message: Message) -> None:
    """
    Выполнение команды /start

    :param bot: объект бота, необходим для взаимодействия с пользователем.
    :param message: переданное сообщение от пользователя.
    """
    keyb = ReplyKeyboardMarkup(resize_keyboard=True)            # Создание "каркаса" клавиатуры

    keyb_button1 = KeyboardButton(button_2)
    keyb_button2 = KeyboardButton(button_3)                     # Инициализация кнопок

    keyb.add(keyb_button1, keyb_button2)                        # Добавление кнопок на клавиатуру
    bot.send_message(message.chat.id, message_2, parse_mode='html')
    bot.send_message(message.chat.id, message_3, parse_mode='html', reply_markup=keyb)
