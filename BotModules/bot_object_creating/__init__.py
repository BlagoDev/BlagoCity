"""
Создание объекта бота

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""

# Импорт библиотек
# Встроенные библиотеки
from os import getenv                       # Получение доступа к .env переменным
# Сторонние библиотеки
from dotenv import load_dotenv              # Выгрузка данных из .env переменны
from telebot import TeleBot                 # Класс бота в Telegram


# Выгружаем файл с важными данными
load_dotenv(r'StaffFiles\kwargs.env')


def bot_object() -> TeleBot:
    """
    Создание объекта бота посредством токена

    :return: bot — объект бота, необходимый для взаимодействия с пользователем.
    """
    return TeleBot(getenv('TOKEN'))
