from flask_mail import Message
from auth_app import mail
from threading import Thread
from auth_app import app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print('message are sended!')

def send_email(subject, sender, recipients, text_body=None, html_body=None):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()