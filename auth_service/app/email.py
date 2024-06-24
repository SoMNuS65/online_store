from flask_mail import Message
from threading import Thread 
from app import app, mail

def async_send_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, body, sender=app.config["MAIL_USERNAME"]):
    msg = Message(subject=subject, recipients=recipients, sender=sender)
    msg.body = body
    thread = Thread(target=async_send_email, args=[app, msg])
    thread.start()