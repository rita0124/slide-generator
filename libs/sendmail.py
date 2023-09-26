import re
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender:

    def __init__(self, title=None, content=None, revicer_addr=None):
        # 從指定路徑讀取信箱登入資訊
        cfg = ConfigParser()
        cfg.read('users/mail.ini')
        # 設定信件內文格式
        self.content = MIMEMultipart()
        self.host = cfg['DEFAULT']['Host']
        self.sender = cfg['DEFAULT']['SenderAddress']
        self.sender_secret = cfg['DEFAULT']['SenderSecret']
        if not revicer_addr:
            receiver_str = cfg['DEFAULT']['ReceiverAddress']
        else:
            receiver_str = reciver_addr
        self.receiver = re.findall(r"[\w\+]+@\w+[^,\s]*", receiver_str)
        # Setup receiver(s)
        self.content['from'] = self.sender
        self.content['to'] = ','.join(self.receiver)

        # Load mail title if value
        if title:
            self.content['subject'] = title
        else:
            self.content['subject'] = 'Asana 工作彙整'

        # Load mail content if value
        if content:
            self.content.attach(MIMEText(content, 'plain', 'utf-8'))

    def set_content(self, mail_content):
        self.content.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    def send_mail(self):
        with smtplib.SMTP(host=self.host) as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()
                #smtp.starttls()
                smtp.login(self.sender, self.sender_secret)
                smtp.send_message(self.content)
                print("Send to: "+str(self.receiver))
                smtp.close()
            except Exception as e:
                print("Error message: ", e)
