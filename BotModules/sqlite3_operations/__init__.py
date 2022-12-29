"""
Выполнение скриптов SQL

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""
# Импорт библиотек
# Встроенные библиотеки
from typing import Any, Union                               # Типы данных для аннотаций
from string import Template                                 # Шаблон для текста письма
from sqlite3 import connect, Cursor, Connection, Error      # Функции, классы и ошибки для работы с SQLite


# Декораторы для подключения к БД
def connection_with_two_args(func) -> Any:
    """
    Декоратор для подключения к БД SQLite с двумя аргументами функции
    """
    def get_connection(arg1, arg2):
        sqlite3_connect = None
        try:
            sqlite3_connect = connect('tickets.db')              # Подключаемся к БД
            func(arg1, arg2, sqlite3_connect)                    # Считываем и выполняем скрипт
            sqlite3_connect.close()                              # Закрываем соединение с БД
        except Error as error:
            print('Ошибка при подключении к sqlite!', error)
            if sqlite3_connect:                                  # Если подключение установлено
                sqlite3_connect.close()                          # Закрываем соединение с БД
    return get_connection


def connection_with_one_arg(func) -> Any:
    """
    Декоратор для подключения к БД SQLite с одним аргументом функции
    """
    def get_connection(arg1):
        sqlite3_connect = None
        try:
            sqlite3_connect = connect('tickets.db')              # Подключаемся к БД
            func(arg1, sqlite3_connect)                          # Считываем и выполняем скрипт
            sqlite3_connect.close()                              # Закрываем соединение с БД
        except Error as error:
            print('Ошибка при подключении к sqlite!', error)
            if sqlite3_connect:                                  # Если подключение установлено
                sqlite3_connect.close()                          # Закрываем соединение с БД
    return get_connection


def connection_without_args(func) -> Any:
    """
    Декоратор для подключения к БД SQLite без аргументов функции
    """
    def get_connection():
        sqlite3_connect = None
        try:
            sqlite3_connect = connect('tickets.db')              # Подключаемся к БД
            func(sqlite3_connect)                                # Считываем и выполняем скрипт
            sqlite3_connect.close()                              # Закрываем соединение с БД
        except Error as error:
            print('Ошибка при подключении к sqlite!', error)
            if sqlite3_connect:                                  # Если подключение установлено
                sqlite3_connect.close()                          # Закрываем соединение с БД
    return get_connection


def exec_script(con: Connection, script: str) -> None:
    """
    Выполнение скрипта SQL

    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    :param script: скрипт SQL для выполнения.
    """
    cursor: Cursor = con.cursor()                   # Курсор для выполнения скрипта
    cursor.execute(script)                          # Выполняем скрипт
    con.commit()                                    # Подтверждаем выполнение
    cursor.close()                                  # Закрываем соединение с курсором


def exec_script_with_unknown_params(con: Connection, script: str, data: Union[tuple, int]) -> None:
    """
    Выполнение скрипта SQL с неизвестными параметрами

    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    :param script: скрипт SQL для выполнения.
    :param data: данные для подстановки.
    """
    cursor: Cursor = con.cursor()                   # Курсор для выполнения скрипта
    cursor.execute(script, data)                    # Выполняем скрипт
    con.commit()                                    # Подтверждаем выполнение
    cursor.close()                                  # Закрываем соединение с курсором


@connection_without_args
def create_table(con: Connection = None) -> None:
    """
    Создание таблицы в БД

    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/create_tickets_table.sql', 'r') as f:
        script = f.read()
    exec_script(con, script)


@connection_with_one_arg
def insert_user_id(user_id: int, con: Connection = None) -> None:
    """
    Вставка ID пользователя в БД

    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_user_id.sql', 'r') as f:
        raw_script: Template = Template(f.read())                   # Создаём шаблон для скрипта
        script: str = raw_script.substitute(user_id_ph=user_id)     # Заполняем шаблон данными
    exec_script(con, script)


@connection_with_two_args
def insert_user_nickname(user_nickname: str, user_id: int, con: Connection = None) -> None:
    """
    Вставка никнейма пользователя в БД

    :param user_nickname: никнейм пользователя в Telegram.
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_user_nickname.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (user_nickname, user_id))


@connection_with_two_args
def insert_ticket_topic(ticket_topic: str, user_id: int, con: Connection = None) -> None:
    """
    Вставка темы заявки в БД

    :param ticket_topic: тема заявки.
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_ticket_topic.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (ticket_topic, user_id))


@connection_with_two_args
def insert_ticket_desc(ticket_desc: str, user_id: int, con: Connection = None) -> None:
    """
    Вставка описания заявки в БД

    :param ticket_desc: описание заявки.
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_ticket_desc.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (ticket_desc, user_id))


@connection_with_two_args
def insert_ticket_coordinates(ticket_coordinates: str, user_id: int, con: Connection = None) -> None:
    """
    Вставка данных координат (широта, долгота) в БД

    :param ticket_coordinates: строка с широтой и долготой (пример: "55.7522200 37.6155600").
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_ticket_coordinates.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (ticket_coordinates, user_id))


@connection_with_two_args
def insert_ticket_file(ticket_file: bytes, user_id: int, con: Connection = None) -> None:
    """
    Вставка данных о файле в таблицу

    :param ticket_file: прочтённый файл изображения или видео (в виде байтов).
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_ticket_file.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (ticket_file, user_id))


@connection_with_two_args
def insert_ticket_file_ext(ticket_file_ext: str, user_id: int, con: Connection = None) -> None:
    """
    Вставка данных о файле в таблицу

    :param ticket_file_ext: расширение файла заявки.
    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/insert_ticket_file_ext.sql', 'r') as f:
        script: str = f.read()
    exec_script_with_unknown_params(con, script, (ticket_file_ext, user_id))


@connection_with_one_arg
def delete_ticket_from_table(user_id: int, con: Connection = None) -> None:
    """
    Удалить заявку из БД

    :param user_id: ID пользователя в Telegram.
    :param con: подключение к БД, выполняется автомотически, прописывать НЕ НАДО.
    """
    with open(r'BotModules/SQLite3 Scripts/delete_from_table.sql', 'r') as f:
        raw_script: Template = Template(f.read())                   # Создаём шаблон для скрипта
        script: str = raw_script.substitute(user_id_ph=user_id)     # Заполняем шаблон данными
    exec_script(con, script)


def select_data_from_table(user_id: int) -> Union[list, None]:
    # Данная функция и декоратор connection_with_one_arg объединены,
    # так как декоратор не позволяет нормально использовать return
    """
    Возвращает данные из таблицы

    :return: result — данные из таблицы.
    """
    sqlite3_connect = None
    try:
        sqlite3_connect = connect('tickets.db')                         # Подключаемся к БД
        with open(r'BotModules/SQLite3 Scripts\select_data_from_table.sql', 'r') as f:
            raw_script: Template = Template(f.read())                   # Создаём шаблон для скрипта
            script: str = raw_script.substitute(user_id_ph=user_id)     # Заполняем шаблон данными
        cursor: Cursor = sqlite3_connect.cursor()                       # Курсор для выполнения скрипта
        cursor.execute(script)                                          # Выполняем скрипт
        sqlite3_connect.commit()                                        # Подтверждаем выполнение
        result = cursor.fetchall()                                      # Извлекаем выходные данные
        sqlite3_connect.close()                                         # Закрываем соединение с БД
        return result
    except Error as error:
        print('Ошибка при подключении к sqlite!', error)
        if sqlite3_connect:
            sqlite3_connect.close()                                     # Закрываем соединение с БД
