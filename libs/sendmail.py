import os
import re
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender:

    def __init__(self, title=None, content=None, receiver_addr=None):
        self.content = MIMEMultipart()
        self.set_content(title, content, receiver_addr)

    def set_attachment(self, filename):
        print("going to attach file")
        with open(filename, 'rb') as f:
            attachment = MIMEText(f.read(), 'base64', 'utf-8')
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            self.content.attach(attachment)
        print("attach function completed")

    def set_content(self, title, mail_content, receiver_addr):
        # 從指定路徑讀取信箱登入資訊
        #cfg = ConfigParser()
        #cfg.read('users/mail.ini')
        # 設定信件內文格式
        #self.host = cfg['DEFAULT']['Host']
        #self.sender = cfg['DEFAULT']['SenderAddress']
        #self.sender_secret = cfg['DEFAULT']['SenderSecret']
        self.host = os.environ['MAIL_SERVER']
        self.sender = os.environ['MAIL_SENDER']
        self.sender_secret = os.environ['MAIL_SENDER_SECRET']
        if receiver_addr is None:
            receiver_str = os.environ['MAIL_RECEIVER']
        else:
            receiver_str = receiver_addr
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
        if mail_content is not None:
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
