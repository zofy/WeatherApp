import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from_address = 'zofy11@gmail.com'
# to_address = 'zofy11@gmail.com'
# text = 'test message sent from Python'
# username = 'xxxxx'
# password = 'xxxxx'
# msg = MIMEMultipart()
# msg['From'] = from_address
# msg['To'] = to_address
# msg['Subject'] = 'Weather forecast'
# msg.attach(MIMEText(text))
# server = smtplib.SMTP('smtp.gmail.com:587')
# server.ehlo()
# server.starttls()
# server.ehlo()
# server.login(username, password)
# server.sendmail(from_address, to_address, msg.as_string())
# server.quit()


class MailManager(object):
    from_address = 'mbforecast@gmail.com'
    username = 'mbforecast'
    password = 'kriziceq'

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

    def send_forecast(self):
        self.server.sendmail(MailManager.from_address, self.to_address, self.msg.as_string())
        self.server.quit()


# m = MailManager('zofy11@gmail.com', 'Ahoj')
# m.login_to_server()
# m.send_forecast()
