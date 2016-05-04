import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailManager(object):
    from_address = 'mbforecast@gmail.com'
    username = 'mbforecast'
    password = 'xxxxxxxx'

    def __init__(self, to_address, text=''):
        self.to_address = to_address
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.text = text
        self.msg = MIMEMultipart()
        self.msg['From'] = MailManager.from_address
        self.msg['To'] = to_address
        self.msg['Subject'] = 'Weather forecast'
        self.msg.attach(MIMEText(text))

    def login_to_server(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(MailManager.username, MailManager.password)

    def send_mail(self):
        self.server.sendmail(MailManager.from_address, self.to_address, self.msg.as_string())
        self.server.quit()
