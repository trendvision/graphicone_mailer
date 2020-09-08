import smtplib
import ssl
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


s_email = os.environ['EMAIL']
s_pass = os.environ['EMAIL_PASS']

s_server = os.environ['SMTP_SERVER']
s_port = int(os.environ['SMTP_PORT'])


def send_email_for_reload_password(receiver_email, temp_password, sender_email=s_email, password=s_pass,
                                   server=s_server, port=s_port):
    """Функция предназначена для отправки E-mail сообщений для воостановления пароля. Не взвращает никакого ответа

        Input:
            receiver_email      -- Email получателя. Адрес на который будет отправлено письмо с временным паролем
            temp_password       -- Временный пароль
            sender_email        -- Email отправителя. Адрес с котрого будет отправлено письмо. Связан с server
            password            -- Пароль для email с котрого будет производиться отправка
            server              -- SMTP-сераер для отпраки сообщений
            port                -- Порт для подкоючения к server
            """

    if password == '':
        print('Password for sender e-mail does not specified')
        return None

    subject = "Refreshing password in GraphicOne"
    body = """
    You receive this email because you try to refresh your password in GraphicOne mobile app.

    Your temporary password: 
    {}
    It will be valid 1 day after sending date in the header of this e-mail.

    In best regards
    GraphicOne team""".format(temp_password)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


# ToDo: Переделать всю отправку email на этот код
def send_email(receiver_email, text, subject, sender_email=s_email, password=s_pass, server=s_server, port=s_port):
    """Функция предназначена для отправки E-mail сообщений для воостановления пароля. Не взвращает никакого ответа

        Input:
            receiver_email      -- Email получателя. Адрес на который будет отправлено письмо с временным паролем
            text                -- Тело сообщения
            subject             -- Тема сообщения
            sender_email        -- Email отправителя. Адрес с котрого будет отправлено письмо. Связан с server
            password            -- Пароль для email с котрого будет производиться отправка
            server              -- SMTP-сераер для отпраки сообщений
            port                -- Порт для подкоючения к server
            """

    # Проверка на то, введен ли пароль для отправки сообщений
    if password == '':
        print('Password for sender e-mail does not specified')
        return None
    # Вводим константы
    body = text

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email

    context = ssl.create_default_context()
    with smtplib.SMTP(server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
