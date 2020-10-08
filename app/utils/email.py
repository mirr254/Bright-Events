import os
from flask_mail import Message
from app import createApp,mail

#mail = Mail( createApp(conf_name=os.getenv('APP_SETTINGS')))

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=createApp(conf_name=os.getenv('APP_SETTINGS')).config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)