import smtplib
import ssl
import traceback
import os

import stringcase


def check_page_number(page_number):
    if page_number is not None:
        try:
            page_number = int(page_number) if int(page_number) > 0 else None
        except ValueError:
            page_number = None
    return page_number


def to_json(o):
    return {stringcase.camelcase(k): v for k, v in vars(o).items()}


def serialize_list(unserialized_list):
    serialized_list = []
    for element in unserialized_list:
        serialized_list.append(to_json(element))
    return serialized_list


def send_email(exception, traceback_message):
    print("Sending email...")
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "recruit.recruiters.problems@gmail.com"
    receiver_email = "recruit.recruiters.problems@gmail.com"
    password = os.getenv('EMAIL_PASSWORD')
    subject = "Exception thrown"
    text = f"""
    Exception called {exception} was caught.
    {traceback_message}
    """
    message = 'Subject: {}\n\n{}'.format(subject, text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
