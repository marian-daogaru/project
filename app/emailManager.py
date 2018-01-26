import os, time, uuid, datetime
from string import Template
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import email.message
import smtplib
from itsdangerous import URLSafeTimedSerializer

from app import app, db
import config
from privateData import *
import models


class SignUpEM(object):
    def __init__(self):
        pass

    def readTemplate(self, filename):
        path = os.path.join(os.getcwd(), filename)
        with open(path, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def generateTemplate(self, user):
        passwordResetSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = passwordResetSerializer.dumps(user.email, salt='password-reset-salt')
        print(token)
        template = self.readTemplate('app/templates/emailConfirmationEmail.html')
        body = template.substitute(SIGNUP_URL = 'http://localhost:5000/confirm/{}'.format(token))
        return body

    def sendConfirmationEmail(self, user):
        msg = MIMEMultipart('related')
        msg['From'] = MAIL_USERNAME
        msg['To'] = user.email
        msg['Subject'] = 'Confirm email'
        body = self.generateTemplate(user)
        body = MIMEText(body, 'html')
        msg.attach(body)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print('message sent')



class PasswordResetEM(object):
    def __init__(self):
        pass

    def readTemplate(self, filename):
        path = os.path.join(os.getcwd(), filename)
        with open(path, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def generateTemplate(self, user):
        passwordResetSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = passwordResetSerializer.dumps(user.email, salt='password-reset-salt')
        print(token)
        template = self.readTemplate('app/templates/resetPasswordEmail.html')
        body = template.substitute(RESET_URL = 'http://localhost:5000/reset/{}'.format(token))
        print(body)
        return body

    def sendResetEmail(self, user):
        msg = MIMEMultipart('related')
        msg['From'] = MAIL_USERNAME
        msg['To'] = user.email
        msg['Subject'] = 'Reset Password'
        body = self.generateTemplate(user)
        body = MIMEText(body, 'html')
        msg.attach(body)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print('message sent')
