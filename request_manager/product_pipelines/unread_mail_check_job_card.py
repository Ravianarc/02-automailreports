#!/usr/bin/python
import email
import imaplib
import datetime
import re
import os
import json

from validate_email_sender_details_job_card import SenderValidation
#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#

config_file_path:str = os.getcwd() + '/' + 'request_manager/mail_config.json'


ADDRESS_PATTERN = re.compile('<(.*?)>')

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


class EmailClient:
    def __init__(self) -> None:
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
        self.email_message = None
        self.emailloadinself =None
    

    def login_to_server(self,imap_server,imap_port,username,password):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL(self.imap_server,self.imap_port)
                r, d = self.imap.login(self.username, self.password)
                assert r == 'OK', 'login failed'
                print(" > Sign as ", d)
            except:
              print("Error")
              break
            # self.imap.logout()
            break
        return self


    def logout(self):
        return self.imap.logout()
    
    
    def list_folders(self):
        response_code, folders = self.imap.list()
        print(response_code)  # OK
        print('Available folders(mailboxes) to select:')
        for folder_details_raw in folders:
            folder_details = folder_details_raw.decode().split()
            print(f'- {folder_details[-1]}')
    
    
    def mail_read(self,ids):
        email_message: list =[]
        self.imap.select('Inbox')
        for id in ids:
            result, email_data = self.imap.fetch(id, "(RFC822)")
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message.append(email.message_from_string(raw_email_string))
        self.email_message = email_message
        return True


    def message_walk(self,email_message=None):
        msg_list =None
        if self.email_message != None :
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    emailBody = part.get_payload(decode=True)
                    message:str =  emailBody.decode('utf-8')
                    msg_list = message.split('\r\n')
                else:
                    continue

            return msg_list
        else:
            return msg_list

    def message_slpit(self,message):
        report_details ={}
        for msg in message:
            print(len(msg))
            report_msg_part = msg.split(':')
            report_details[report_msg_part[0]]= report_msg_part[1]
        return report_details

    def get_message_loaded_status(self):
        return self.emailloadinself

    def get_email_message(self):
        return self.email_message


    def get_recipients(self,email_message):
        recipients = {}
        addr_fields = ['From', 'To', 'Cc', 'Bcc']

        for f in addr_fields:
            rfield = email_message.get(f, "")
            rlist = re.findall(ADDRESS_PATTERN, rfield)
            if len(rlist) != 0 :
                recipients[f] = rlist[0]
        return recipients


    def get_unread_Ids(self):
        self.imap.select()
        response_code, d = self.imap.search(None, "UNSEEN")
        print(response_code)
        return(d)



    def load_unread(self):
        list = self.get_unread_Ids()
        unreadmail = len(list[0].split())
        print(unreadmail)
        # if any unread mail available
        if unreadmail >= 1:
            latest_id = list[0].split()
            print('Exchange has unread email id',latest_id)
            emailloadinself=self.mail_read(latest_id)
            if emailloadinself:
                self.emailloadinself = True
                print('Emails loaeded from exchange to emailclient')
                return True
        else:
            print('Unread email NOT in account'  )
            self.emailloadinself = False
            return  False

    def unread_mail_check_job_card(self):
        conf=CollectConfiguration().configuration()
        IMAP_SERVER = conf["IMAP_SERVER"]
        IMAP_PORT = conf["IMAP_PORT"]
        USERNAME =conf["USERNAME"]
        PASSWROD =conf["PASSWROD"]
        email_cleint_self = self.login_to_server(IMAP_SERVER,IMAP_PORT,USERNAME,PASSWROD)
        has_unread_email_in_client = email_cleint_self.load_unread()
        return  self


if __name__ =='__main__':
    email_cleint_self = EmailClient()
    msg_list =['Report name : test', 'parameter : { from date = 123 , two_date=456}', 'type:existing','query:select * from table where id="2"']
    report_details = email_cleint_self.message_slpit(msg_list)
    print(report_details)
#    email_cleint_self = EmailClient().unread_mail_check_job_card()
#    if email_cleint_self.get_message_loaded_status():
#        email_message = email_cleint_self.get_email_message()
#        for message in email_message:
#            recipients = email_cleint_self.get_recipients(message)
#            print(recipients)
#            msg_list= email_cleint_self.message_walk(message)
#    else:
#        print('Unread Message Not loaded')
#    email_cleint_self.logout()
