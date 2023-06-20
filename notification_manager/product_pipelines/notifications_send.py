#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
import os
import datetime
import json

config_file_path:str = os.getcwd() + '/' + 'notification_manager/mail_config.json'


class CollectConfiguration:
    def __int__(self):
        pass

    def configuration(self):
        try :
            f = open(config_file_path)
            data = json.load(f)
            return (data)
        except Exception as e:
            print(f'caught {type(e)}: e')

class SentNotificationEmailClient:
    def __int__(self):
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
        self.SMTP_SERVER
        self.SMTP_PORT
        self.USERNAME
        self.PASSWROD
        self.msg
        self.emailid

    def create_email(self):
        # Create email message with HTML content
        subject = 'Update on your report request!'
        body = ('<h1>Update on your report request.</h1>'
                '<p> <strong>' + self.msg +'</strong> and may be an <em>attachment</em>.</p>')
        msg = MIMEMultipart()
        msg['From'] = self.USERNAME
        msg['To'] = self.emailid
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        return  msg

    def attachement (self,msg,attachement):
        # Add an attachment
        attachment_path = 'example_file.pdf'
        attachment_filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
            msg.attach(attachment)
        return msg

    def send_notificaiton_job_card(self , msg , mail_id , attachement = None):
        conf=CollectConfiguration().configuration()
        self.SMTP_SERVER  = conf["SMTP_SERVER"]
        self.SMTP_PORT = conf["SMTP_PORT"]
        self.USERNAME =conf["USERNAME"]
        self.PASSWROD =conf["PASSWROD"]
        self.msg = msg
        self.emailid = mail_id
        email = self.create_email()

        # Send email
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.USERNAME, self.PASSWROD)
            server.send_message(email)
        print('Email sent successfully!')

if __name__ == '__main__':
    SentNotificationEmailClient().send_notificaiton_job_card('hi','manovairavi@hotmail.com')
