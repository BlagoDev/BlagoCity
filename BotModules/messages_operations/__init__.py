"""
Проверка текста на "нажатие" кнопок

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""

# Импорт библиотек
# Встроенные библиотеки
from os import getenv                                                                   # Получение доступа к .env переменным
from string import Template                                                             # Шаблон для текста письма
# Сторонние библиотеки
from dotenv import load_dotenv                                                          # Выгрузка данных из .env переменных
from telebot import TeleBot                                                             # Класс бота в Telegram
from telebot.types import Message, \
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto                                                      # Типы данных для грамотного использования Telegram
# Модули для исполнения кода
from BotModules.bot_object_creating import bot_object
from BotModules.sqlite3_operations import insert_user_id, insert_user_nickname, \
    insert_ticket_topic, insert_ticket_desc, \
    insert_ticket_coordinates, insert_ticket_file, \
    insert_ticket_file_ext, select_data_from_table
# Глобализация переменных
global ticket_topic


# Загружаем изображения для отправки
path: str = r'StaffFiles/Screenshots/NicknameInstruction'

with open(path+'/1.jpg', 'rb') as f:
    nickname_instruction1 = InputMediaPhoto(f.read())
with open(path+'/2.jpg', 'rb') as f:
    nickname_instruction2 = InputMediaPhoto(f.read())
with open(path+'/3.jpg', 'rb') as f:
    nickname_instruction3 = InputMediaPhoto(f.read())
with open(path+'/4.jpg', 'rb') as f:
    nickname_instruction4 = InputMediaPhoto(f.read())


# Выгружаем файл с кнопками и сообщениями
load_dotenv(r'StaffFiles\message_text.env')

# Для редактирования текста кнопок и сообщений
# откройте файл message_text.env в папке StaffFiles и измените интересующую
# вас переменную!
# (Естественно, на Github'е этой папки не будет)

# КНОПКИ
# Кнопки: вернуться в главное меню
button_1: str = getenv('BUTTON_1')

# Кнопки: главное меню
button_2: str = getenv('BUTTON_2')
button_3: str = getenv('BUTTON_3')

# Кнопки: тип заявки
button_4: str = getenv('BUTTON_4')
button_5: str = getenv('BUTTON_5')
button_6: str = getenv('BUTTON_6')
button_7: str = getenv('BUTTON_7')

# Кнопки: FAQ
button_8: str = getenv('BUTTON_8')
button_9: str = getenv('BUTTON_9')
button_ask_owner: str = getenv('BUTTON_ASK_OWNER')
button_github: str = getenv('BUTTON_GITHUB')

# Кнопки: благоустройство
button_10: str = getenv('BUTTON_10')
button_11: str = getenv('BUTTON_11')
button_12: str = getenv('BUTTON_12')
button_13: str = getenv('BUTTON_13')
button_14: str = getenv('BUTTON_14')
button_15: str = getenv('BUTTON_15')

# Кнопки: правонарушение
button_16: str = getenv('BUTTON_16')
button_17: str = getenv('BUTTON_17')
button_18: str = getenv('BUTTON_18')

# Кнопки: предложение
button_19: str = getenv('BUTTON_19')
button_20: str = getenv('BUTTON_20')
button_21: str = getenv('BUTTON_21')
button_22: str = getenv('BUTTON_22')
button_23: str = getenv('BUTTON_23')
button_24: str = getenv('BUTTON_24')

# Кнопки: авария
button_25: str = getenv('BUTTON_25')
button_26: str = getenv('BUTTON_26')

# Кнопки: запрос местоположения
button_27: str = getenv('BUTTON_27')

# Кнопки: выбор отправки файла
button_28: str = getenv('BUTTON_28')
button_29: str = getenv('BUTTON_29')

# Кнопки: отправка заявки
button_30: str = getenv('BUTTON_30')
button_31: str = getenv('BUTTON_31')

# Кнопки: режим пользователя
button_32: str = getenv('BUTTON_32')
button_33: str = getenv('BUTTON_33')
button_34: str = getenv('BUTTON_34')

# Кнопки: вернуться в меню выбора темы
button_35: str = getenv('BUTTON_35')

# СООБЩЕНИЯ
message_1: str = getenv('MESSAGE_1')

message_3: str = getenv('MESSAGE_3')

message_4: str = getenv('MESSAGE_4')

message_5: str = getenv('MESSAGE_5')

message_6: str = getenv('MESSAGE_6')

message_7: str = getenv('MESSAGE_7')

message_8: str = getenv('MESSAGE_8')
message_9: str = getenv('MESSAGE_9')

message_10: str = getenv('MESSAGE_10')

message_11: str = getenv('MESSAGE_11')

message_12: str = getenv('MESSAGE_12')

message_13: str = getenv('MESSAGE_13')

message_14: str = getenv('MESSAGE_14')
message_15: str = getenv('MESSAGE_15')
message_16: str = getenv('MESSAGE_16')

message_20: str = getenv('MESSAGE_20')
message_21: str = getenv('MESSAGE_21')
message_22: str = getenv('MESSAGE_22')

message_23_raw: Template = Template(getenv('MESSAGE_23'))      # Шаблон сообщения

message_24: str = getenv('MESSAGE_24')

message_25: str = getenv('MESSAGE_25')

# Выгружаем файл с важными данными
load_dotenv(r'StaffFiles\kwargs.env')

dev_contact: str = getenv('DEV_CONTACT')
# Подставляем данные к шаблону
message_23 = message_23_raw.substitute(DEV_CONTACT=dev_contact)


def check_messages(bot: TeleBot, message: Message) -> None:
    """
    Проверка пользовательского текста на наличие текста кнопок

    :param bot: объект бота, необходим для взаимодействия с пользователем.
    :param message: переданное сообщение от пользователя.
    """
    # Глобализация переменных
    global ticket_topic

    mes = message.text                        # Текст сообщения пользователя
    # Главное меню
    if mes == button_2:
        user_id = message.from_user.id        # ID пользователя
        insert_user_id(user_id)               # Записываем ID в БД с заявкой

        keyb = ReplyKeyboardMarkup(resize_keyboard=True)          # Создание "каркаса" клавиатуры

        keyb_button1 = KeyboardButton(button_32)
        keyb_button2 = KeyboardButton(button_33)                  # Инициализация кнопок
        keyb_button3 = KeyboardButton(button_34)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3)                                    # Добавление кнопок
        bot.send_message(message.chat.id, message_20, parse_mode='html', reply_markup=keyb)
    elif mes == button_3:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_8)
        keyb_button2 = KeyboardButton(button_9)
        keyb_button3 = KeyboardButton(button_ask_owner)
        keyb_button4 = KeyboardButton(button_github)
        back_to_menu_button = KeyboardButton(button_1)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        keyb.add(back_to_menu_button)
        bot.send_message(message.chat.id, message_6, parse_mode='html', reply_markup=keyb)

    # FAQ
    elif mes == button_8:
        bot.send_message(message.chat.id, message_8, parse_mode='html')
    elif mes == button_9:
        bot.send_message(message.chat.id, message_9, parse_mode='html')
    elif mes == button_ask_owner:
        bot.send_message(message.chat.id, message_23, parse_mode='html')
    elif mes == button_github:
        bot.send_message(message.chat.id, message_25, parse_mode='html')

    # Типы заявок
    elif mes == button_4:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_10)
        keyb_button2 = KeyboardButton(button_11)
        keyb_button3 = KeyboardButton(button_12)
        keyb_button4 = KeyboardButton(button_13)
        keyb_button5 = KeyboardButton(button_14)
        keyb_button6 = KeyboardButton(button_15)
        back_to_topic_choice = KeyboardButton(button_35)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        keyb.add(keyb_button5, keyb_button6)
        keyb.add(back_to_topic_choice)
        bot.send_message(message.chat.id, message_5, parse_mode='html', reply_markup=keyb)
    elif mes == button_5:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_16)
        keyb_button2 = KeyboardButton(button_17)
        keyb_button3 = KeyboardButton(button_18)
        back_to_topic_choice = KeyboardButton(button_35)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3)
        keyb.add(back_to_topic_choice)
        bot.send_message(message.chat.id, message_5, parse_mode='html', reply_markup=keyb)
    elif mes == button_6:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_19)
        keyb_button2 = KeyboardButton(button_20)
        keyb_button3 = KeyboardButton(button_21)
        keyb_button4 = KeyboardButton(button_22)
        keyb_button5 = KeyboardButton(button_23)
        keyb_button6 = KeyboardButton(button_24)
        back_to_topic_choice = KeyboardButton(button_35)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        keyb.add(keyb_button5, keyb_button6)
        keyb.add(back_to_topic_choice)
        bot.send_message(message.chat.id, message_5, parse_mode='html', reply_markup=keyb)
    elif mes == button_7:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_25)
        keyb_button2 = KeyboardButton(button_26)
        back_to_topic_choice = KeyboardButton(button_35)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(back_to_topic_choice)
        bot.send_message(message.chat.id, message_5, parse_mode='html', reply_markup=keyb)

    # Выбор конечной темы заявки
    elif mes == button_10:
        user_id: int = message.from_user.id                         # ID пользователя в Telegram
        ticket_topic = button_10                                    # Задаём тему заявки
        insert_ticket_topic(ticket_topic, user_id)                  # Записываем тему в БД с заявкой

        keyb = ReplyKeyboardRemove()                                # Убираем клавиатуру
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)    # Вызываем функцию с считыванием описания
    elif mes == button_11:
        user_id: int = message.from_user.id
        ticket_topic = button_11
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_12:
        user_id: int = message.from_user.id
        ticket_topic = button_12
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_13:
        user_id: int = message.from_user.id
        ticket_topic = button_13
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_14:
        user_id: int = message.from_user.id
        ticket_topic = button_14
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_15:
        user_id: int = message.from_user.id
        ticket_topic = button_15
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_16:
        user_id: int = message.from_user.id
        ticket_topic = button_16
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_17:
        user_id: int = message.from_user.id
        ticket_topic = button_17
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_18:
        user_id: int = message.from_user.id
        ticket_topic = button_18
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_19:
        user_id: int = message.from_user.id
        ticket_topic = button_19
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_20:
        user_id: int = message.from_user.id
        ticket_topic = button_20
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_21:
        user_id: int = message.from_user.id
        ticket_topic = button_21
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_22:
        user_id: int = message.from_user.id
        ticket_topic = button_22
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_23:
        user_id: int = message.from_user.id
        ticket_topic = button_23
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_24:
        user_id: int = message.from_user.id
        ticket_topic = button_24
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_25:
        user_id: int = message.from_user.id
        ticket_topic = button_25
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)
    elif mes == button_26:
        user_id: int = message.from_user.id
        ticket_topic = button_26
        insert_ticket_topic(ticket_topic, user_id)

        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_7, parse_mode='html', reply_markup=keyb)
        bot.register_next_step_handler(message, set_ticket_desc)

    # Выбор отправки файла
    elif mes == button_28:
        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_12, parse_mode='html', reply_markup=keyb)
    elif mes == button_29:
        keyb = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, message_24, parse_mode='html', reply_markup=keyb)
        accept_ticket(message)                                      # Отправляем запрос на подтверждение заявки

    # Выбор режима пользователя
    elif mes == button_32:
        user_id = message.from_user.id                              # ID пользователя в Telegram
        user_nickname = message.from_user.username                  # Имя пользователя
        insert_user_nickname(user_nickname, user_id)                # Записываем никнейм в БД с заявкой

        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_4)
        keyb_button2 = KeyboardButton(button_5)
        keyb_button3 = KeyboardButton(button_6)
        keyb_button4 = KeyboardButton(button_7)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        bot.send_message(message.chat.id, message_21, parse_mode='html')
        bot.send_message(message.chat.id, message_4, parse_mode='html', reply_markup=keyb)
    elif mes == button_33:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_4)
        keyb_button2 = KeyboardButton(button_5)
        keyb_button3 = KeyboardButton(button_6)
        keyb_button4 = KeyboardButton(button_7)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        bot.send_message(message.chat.id, message_21, parse_mode='html')
        bot.send_message(message.chat.id, message_4, parse_mode='html', reply_markup=keyb)
    elif mes == button_34:
        instruction = bot.send_message(message.chat.id, message_22, parse_mode='html')
        bot.send_media_group(message.chat.id, [
            nickname_instruction1,
            nickname_instruction2,
            nickname_instruction3,                                      # Отправляем скриншоты с инструкциями
            nickname_instruction4
            ], reply_to_message_id=instruction.id)

    # Вернуться в главное меню
    elif mes == button_1:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_2)
        keyb_button2 = KeyboardButton(button_3)

        keyb.add(keyb_button1, keyb_button2)
        bot.send_message(message.chat.id, message_3, parse_mode='html', reply_markup=keyb)

    # Вернуться в меню выбора темы
    elif mes == button_35:
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_4)
        keyb_button2 = KeyboardButton(button_5)
        keyb_button3 = KeyboardButton(button_6)
        keyb_button4 = KeyboardButton(button_7)

        keyb.add(keyb_button1, keyb_button2)
        keyb.add(keyb_button3, keyb_button4)
        bot.send_message(message.chat.id, message_4, parse_mode='html', reply_markup=keyb)

    # Сообщение от пользователя, не совпадающее с кнопками, или неожиданный ввод
    else:
        bot.send_message(message.chat.id, message_1, parse_mode='html')


def set_ticket_desc(message: Message) -> None:
    """
    Считывание описания заявки из сообщения

    :param message: переданное сообщение от пользователя.
    """
    user_id: int = message.from_user.id                 # ID пользователя в Telegram
    ticket_desc: str = message.text                     # Описание заявки из текста полученного сообщения
    insert_ticket_desc(ticket_desc, user_id)            # Записываем описание в БД с заявкой

    keyb = ReplyKeyboardMarkup(resize_keyboard=True)
    keyb_button1 = KeyboardButton(button_27, request_location=True)
    back_to_topic_choice = KeyboardButton(button_35)

    keyb.add(keyb_button1)
    keyb.add(back_to_topic_choice)

    bot: TeleBot = bot_object()                         # Инициализируем переменную bot с классом Telegram-бота
    bot.send_message(message.chat.id, message_10, parse_mode='html', reply_markup=keyb)


def set_ticket_coordinates(message: Message) -> None:
    """
    Считывание координат из сообщения

    :param message: переданное сообщение от пользователя.
    """
    user_id: int = message.from_user.id                                                                     # ID пользователя в Telegram
    ticket_coordinates_string: str = f'{message.location.latitude} {message.location.longitude}'            # Строка с координатами метки
    insert_ticket_coordinates(ticket_coordinates_string, user_id)                                           # Записываем координаты в БД с заявкой

    keyb = ReplyKeyboardMarkup(resize_keyboard=True)
    keyb_button1 = KeyboardButton(button_28)
    keyb_button2 = KeyboardButton(button_29)
    back_to_topic_choice = KeyboardButton(button_35)

    keyb.add(keyb_button1, keyb_button2)
    keyb.add(back_to_topic_choice)

    bot: TeleBot = bot_object()                         # Инициализируем переменную bot с классом Telegram-бота
    bot.send_message(message.chat.id, message_11, parse_mode='html', reply_markup=keyb)


def set_ticket_file(message: Message) -> None:
    """
    Считывание файла и его типа из сообщения

    :param message: переданное сообщение от пользователя.
    """
    user_id: int = message.from_user.id         # ID пользователя в Telegram
    bot: TeleBot = bot_object()                 # Инициализируем переменную bot с классом Telegram-бота
    content_type: str = message.content_type    # Тип файла

    # Узнаём расширение и ID файла
    ticket_file_id = None
    ticket_file_ext = None
    if content_type == 'photo':                             # Если файл — фото
        ticket_file_id = message.photo[-1].file_id          # ID файла
        ticket_file_ext = 'png'                             # Расширение файла
    elif content_type == 'video':                           # Если файл — видео
        ticket_file_id = message.video.file_id
        ticket_file_ext = 'mp4'
    elif content_type == 'video_note':                      # Если файл — видеозапись с камеры
        ticket_file_id = message.video_note.file_id
        ticket_file_ext = 'mp4'
    elif content_type == 'audio':                           # Если файл — аудиозапись
        ticket_file_id = message.audio.file_id
        ticket_file_ext = 'mp3'
    elif content_type == 'voice':                           # Если файл — голосовое сообщение
        ticket_file_id = message.voice.file_id
        ticket_file_ext = 'mp3'
    elif content_type == 'document':                        # Если файл — документ (или другой файл, отправленный как документ)
        ticket_file_id = message.document.file_id
        ticket_file_ext = 'pdf'
    ticket_file_info = bot.get_file(ticket_file_id)                                 # Узнаём информацию о файле для скачивания
    ticket_file_data: bytes = bot.download_file(ticket_file_info.file_path)         # Скачиваем файл

    insert_ticket_file(ticket_file_data, user_id)                                   # Записываем файл в БД с заявкой
    insert_ticket_file_ext(ticket_file_ext, user_id)                                # Записываем расширение файла в БД с заявкой
    accept_ticket(message)                                                          # Отправляем запрос на подтверждение заявки


def accept_ticket(message: Message) -> None:
    """
    Отправка сообщения с одтверждением заявки пользователем

    :param message: переданное сообщение от пользователя.
    """
    def send_accept(nickname: str,
                    topic: str,
                    desc: str,
                    latitude: str,
                    longitude: str,
                    file: bytes,
                    ext: str):
        # Инициализируем переменную bot с классом Telegram-бота
        local_bot: TeleBot = bot_object()
        if nickname:                                                        # Если заявка публичная
            status: str = 'Публичная'
        else:                                                               # Если заявка анонимная
            status: str = 'Анонимная'
        if not topic or not desc or not latitude or not longitude:          # Если какой-то из обязательных параметров заявки не заполнен
            local_keyb = ReplyKeyboardMarkup(resize_keyboard=True)

            local_keyb_button1 = KeyboardButton(button_2)
            local_keyb_button2 = KeyboardButton(button_3)

            local_keyb.add(local_keyb_button1, local_keyb_button2)
            local_bot.send_message(message.chat.id, message_13, parse_mode='html', reply_markup=local_keyb)
        else:                                                               # Если все обязательные параметры заполнены
            inl_keyb = InlineKeyboardMarkup()                                                     # Создание "каркаса" Inline-клавиатуры
            inl_keyb.row_width = 2

            inl_keyb_button1 = InlineKeyboardButton(button_30, callback_data='cb_yes')
            inl_keyb_button2 = InlineKeyboardButton(button_31, callback_data='cb_no')             # Инициализация кнопки

            inl_keyb.add(inl_keyb_button1, inl_keyb_button2)                                      # Добавление кнопок на клавиатуру
            if not file:                                                                                                    # Если файл не отправляли
                raw_message: Template = Template(message_14)                                                                # Создаём шаблон для сообщения
                message_to_send: str = raw_message.substitute(ph_0=status, ph_1=topic, ph_2=desc)                           # Заполняем шаблон данными заявки
                local_bot.send_message(message.chat.id, message_to_send, parse_mode='html', reply_markup=inl_keyb)
                local_bot.send_location(message.chat.id, float(latitude), float(longitude))
            else:                                                                                                           # Если файл есть в заявке
                raw_message: Template = Template(message_15)
                message_to_send: str = raw_message.substitute(ph_0=status, ph_1=topic, ph_2=desc)
                local_bot.send_message(message.chat.id, message_to_send, parse_mode='html', reply_markup=inl_keyb)
                local_bot.send_location(message.chat.id, float(latitude), float(longitude))
                # Отправляем файл в зависимости от расширения
                if ext == 'png':
                    local_bot.send_photo(message.chat.id, file)
                elif ext == 'mp4':
                    local_bot.send_video(message.chat.id, file)
                elif ext == 'mp3':
                    local_bot.send_audio(message.chat.id, file)
                elif ext == 'pdf':
                    local_bot.send_document(message.chat.id, file)

    user_id: int = message.from_user.id                                 # ID пользователя в Telegram
    try:
        db_data: list = select_data_from_table(user_id)[-1]             # Получаем данные последней заявки из БД

        user_nickname: str = db_data[1]                                 # Имя пользователя Telegram
        ticket_topic_final: str = db_data[2]                            # Тема
        ticket_desc_final: str = db_data[3]                             # Описание
        coordinates_list: str = db_data[4].split()                      # Координаты метки
        ticket_coordinates_latitude: str = coordinates_list[0]          # Широта
        ticket_coordinates_longitude: str = coordinates_list[1]         # Долгота
        ticket_file: bytes = db_data[5]                                 # Файл
        ticket_file_ext: str = db_data[6]                               # Расширение файла

        # Отправляем заявку на подтверждение
        send_accept(user_nickname,
                    ticket_topic_final,
                    ticket_desc_final,
                    ticket_coordinates_latitude,
                    ticket_coordinates_longitude,
                    ticket_file,
                    ticket_file_ext)
    except IndexError:
        bot: TeleBot = bot_object()
        keyb = ReplyKeyboardMarkup(resize_keyboard=True)

        keyb_button1 = KeyboardButton(button_2)
        keyb_button2 = KeyboardButton(button_3)

        keyb.add(keyb_button1, keyb_button2)
        bot.send_message(message.chat.id, message_13, parse_mode='html', reply_markup=keyb)


def dismiss_ticket(bot: TeleBot, call: CallbackQuery):
    """
    Отклонение заявки

    :param bot: объект бота, необходимый для взаимодействия с пользователем.
    :param call: нажатие на Inline-кнопку.
    """
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=InlineKeyboardMarkup())
    bot.send_message(call.message.chat.id, message_16, parse_mode='html')
    keyb = ReplyKeyboardMarkup(resize_keyboard=True)

    keyb_button1 = KeyboardButton(button_2)
    keyb_button2 = KeyboardButton(button_3)

    keyb.add(keyb_button1, keyb_button2)
    bot.send_message(call.message.chat.id, message_4, parse_mode='html', reply_markup=keyb)
