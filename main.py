"""
Главный исполнительный файл проекта

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""

# Импорт библиотек
# Встроенные библиотеки
from os import getenv                                                               # Получение доступа к .env переменным
# Сторонние библиотеки
from dotenv import load_dotenv                                                      # Выгрузка данных из .env переменных
from telebot import TeleBot                                                         # Класс бота в Telegram
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton                                             # Типы данных для грамотного использования Telegram
# Модули для исполнения кода
from BotModules.bot_object_creating import bot_object                               # Создание класса бота
from BotModules.start_command import start                                          # Выполнение команды /start
from BotModules.messages_operations import check_messages, \
    set_ticket_coordinates, set_ticket_file, dismiss_ticket                        # Операции с сообщениями
from BotModules.send_email import email_sending                                     # Отправка электронного письма с заявкой
from BotModules.sqlite3_operations import delete_ticket_from_table                  # Выполнение скриптов для базы данных SQLite


# Выгружаем файл с кнопками и сообщениями
load_dotenv(r'StaffFiles\message_text.env')

# Для редактирования текста кнопок и сообщений
# откройте файл message_text.env в папке StaffFiles и измените интересующую
# вас переменную!
# (Естественно, на Github'е этой папки не будет)

# КНОПКИ
# Кнопки: главное меню
button_2: str = getenv('BUTTON_2')
button_3: str = getenv('BUTTON_3')


# СООБЩЕНИЯ
message_3: str = getenv('MESSAGE_3')

message_17: str = getenv('MESSAGE_17')
message_18: str = getenv('MESSAGE_18')

message_19: str = getenv('MESSAGE_19')


# Инициализируем переменную bot с классом Telegram-бота
bot: TeleBot = bot_object()


# Функции-обработчики сообщений
@bot.message_handler(commands=['start'])                                        # Команда /start (первое открытие чата)
def start_main(message: Message):
    start(bot, message)


@bot.message_handler(content_types=['text'])                                    # Текстовые сообщения
def text_checking_main(message: Message) -> None:
    check_messages(bot, message)


@bot.message_handler(content_types=['location'])                                # Местоположение от пользователя
def set_ticket_coordinates_main(message: Message) -> None:
    set_ticket_coordinates(message)


@bot.message_handler(content_types=['photo', 'video', 'video_note',
                                    'audio', 'voice', 'document'])              # Типы данных файла пользователя
def set_ticket_file_main(message: Message) -> None:
    set_ticket_file(message)


@bot.callback_query_handler(func=lambda call: True)                             # Нажатие Inline-кнопок
def callback_query(call: CallbackQuery):
    if call.data == 'cb_yes':                               # Если запрос на отправку подтверждён
        bot.answer_callback_query(call.id, message_17)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=InlineKeyboardMarkup())        # Удаление Inline-клавиатуры
        waiting: Message = bot.send_message(call.message.chat.id, message_18, parse_mode='html')

        email_sending(call.from_user.id)                                    # Отправка электронного письма
        delete_ticket_from_table(call.from_user.id)                         # Удаление данных заявки из таблицы

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=waiting.message_id, text=message_19)
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)                    # Создание "каркаса" клавиатуры

        keyb_button1 = KeyboardButton(button_2)
        keyb_button2 = KeyboardButton(button_3)                             # Инициализация кнопок

        keyb.add(keyb_button1, keyb_button2)                                # Добавление кнопок
        bot.send_message(call.message.chat.id, message_3, parse_mode='html', reply_markup=keyb)
    elif call.data == 'cb_no':                              # Если запрос на отправку отменён
        delete_ticket_from_table(call.from_user.id)         # Удаление данных заявки из таблицы
        dismiss_ticket(bot, call)                          # Отправляем пользователя на перезаполнение заявки


bot.infinity_polling()                    # Запуск бота
