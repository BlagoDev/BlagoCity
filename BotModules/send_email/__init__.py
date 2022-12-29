"""
Отправка письма на электронную почту

Copyright 2022 BlagoDev
Licensed under the Apache License, Version 2.0 (the «License»)
"""

# Импорт библиотек
# Встроенные библиотеки
from os import getenv                                                   # Получение доступа к .env переменным
from string import Template                                             # Шаблон для текста письма
from smtplib import SMTP, SMTPException                                 # Подключение к серверу для отправки письма
from email import encoders                                              # Кодировка основы для файла
from email.mime.text import MIMEText                                    # Прикрепение текста к письму
from email.mime.base import MIMEBase                                    # Основа для закреплённого файла
from email.mime.multipart import MIMEMultipart                          # Тело письма
from email.utils import formatdate                                      # Дата письма
# Сторонние библиотеки
from dotenv import load_dotenv                                          # Выгрузка данных из .env переменных
# Модули для исполнения кода
from BotModules.sqlite3_operations import select_data_from_table        # Выполнение скриптов для базы данных SQLite


# Выгружаем файл с кнопками и сообщениями
load_dotenv(r'StaffFiles\message_text.env')

subject: str = getenv('SUBJECT')
maps_link_temp: Template = Template(getenv('MAPS_LINK'))
text_with_file_temp: Template = Template(getenv('TEXT_WITH_FILE'))
text_with_file_anon_temp: Template = Template(getenv('TEXT_WITH_FILE_ANON'))
text_without_file_temp: Template = Template(getenv('TEXT_WITHOUT_FILE'))
text_without_file_anon_temp: Template = Template(getenv('TEXT_WITHOUT_FILE_ANON'))

# Выгружаем файл с важными данными
load_dotenv(r'StaffFiles\kwargs.env')

email_password: str = getenv('EMAIL_PASSWORD')
server_addr: str = getenv('SERVER_ADDR')
port_number: int = int(getenv('PORT_NUMBER'))
from_address: str = getenv('FROM_ADDRESS')
to_address: str = getenv('TO_ADDRESS')


def email_sending(user_id: int) -> None:
    """
    Отправка письма на почту с данными заявки

    :param user_id: ID пользователя в Telegram, по которому будет осуществляться поиск заявки.
    """
    def send(user_nickname: str,
             topic: str,
             desc: str,
             latitude: str,
             longitude: str,
             file: bytes,
             ext: str):
        coordinates_link: str = maps_link_temp.substitute(LONGITUDE=longitude, LATITUDE=latitude)                   # Ссылка на координаты пользователя
        # Заполнение шаблонов текстов
        text_with_file: str = text_with_file_temp.substitute(USER_NICKNAME=user_nickname,
                                                             TOPIC=topic,
                                                             DESC=desc,
                                                             COORDINATES_LINK=coordinates_link)                     # С файлом, публично
        text_with_file_anon: str = text_with_file_anon_temp.substitute(TOPIC=topic,
                                                                       DESC=desc,
                                                                       COORDINATES_LINK=coordinates_link)           # С файлом, анонимно
        text_without_file: str = text_without_file_temp.substitute(USER_NICKNAME=user_nickname,
                                                                   TOPIC=topic,
                                                                   DESC=desc,
                                                                   COORDINATES_LINK=coordinates_link)               # Без файла, публично
        text_without_file_anon: str = text_without_file_anon_temp.substitute(TOPIC=topic,
                                                                             DESC=desc,
                                                                             COORDINATES_LINK=coordinates_link)     # Без файла, анонимно
        server: str = server_addr                       # Адрес сервера почты
        port: int = port_number                         # Номер порта сервера почты
        from_addr: str = from_address                   # Адрес отправителя
        to_addr: str = to_address                       # Адрес получателя
        msg = MIMEMultipart()                           # Солянка из данных письма
        # Добавляем необходимые данные к письму
        msg['From'] = from_addr
        msg['To'] = ','.join(to_addr)
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        if file:                                                  # Если в заявке есть файлы
            if user_nickname:                                     # Если заявка публичная
                msg.attach(MIMEText(text_with_file))
            else:                                                 # Если заявка анонимная
                msg.attach(MIMEText(text_with_file_anon))

            attachment: MIMEBase = MIMEBase('application', 'octet-stream')                                            # Основа для закрепления файла
            header: tuple[str, str] = 'Content-Disposition', f'attachment; filename="User File.{ext}"'                # Информация о файле
            attachment.set_payload(file)
            encoders.encode_base64(attachment)
            attachment.add_header(*header)
            msg.attach(attachment)
        else:                                                     # Если в заявке нет файлов
            if user_nickname:                                     # Если заявка публичная
                msg.attach(MIMEText(text_without_file))
            else:                                                 # Если заявка анонимная
                msg.attach(MIMEText(text_without_file_anon))
        smtp = None
        # Попытка отправки письма
        try:
            smtp = SMTP(server, port)                              # Устанавливаем связь с сервером
            smtp.starttls()                                        # Включаем режим TLS
            smtp.ehlo()                                            # Взаимодействуем с сервером
            smtp.login(from_addr, email_password)                  # Входим в аккаунт почты
            smtp.sendmail(from_addr, to_addr, msg.as_string())     # Отправляем письмо с заявкой
        except SMTPException as err:
            raise err
        finally:
            smtp.quit()

    # Ищем данные заявки в БД и используем их для отправки письма
    db_data: list = select_data_from_table(user_id)[-1]                     # Получаем данные последней заявки из БД

    user_nickname_final: str = db_data[1]                                   # Имя пользователя Telegram
    ticket_topic_final: str = db_data[2]                                    # Тема
    ticket_desc_final: str = db_data[3]                                     # Описание
    coordinates_list: str = db_data[4].split()                              # Координаты метки
    ticket_coordinates_latitude: str = coordinates_list[0]                  # Широта
    ticket_coordinates_longitude: str = coordinates_list[1]                 # Долгота
    ticket_file: bytes = db_data[5]                                         # Файл
    ticket_file_ext: str = db_data[6]                                       # Расширение файла

    # Отправляем письмо с полученными данными
    send(user_nickname_final,
         ticket_topic_final,
         ticket_desc_final,
         ticket_coordinates_latitude,
         ticket_coordinates_longitude,
         ticket_file,
         ticket_file_ext)
