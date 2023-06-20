import os
import sys

# setting envirionment path
pipelines_environment_path:str = os.getcwd() + '/' + 'request_manager/product_pipelines'
if pipelines_environment_path not in sys.path:
    sys.path.append(pipelines_environment_path)


# setting environment path
channel_environment_path:str = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)


from unread_mail_check_job_card import EmailClient
from validate_email_sender_details_job_card import SenderValidation
from notification_line  import NotificationInsert
from create_request_job_card import ReportsRequest

class RequestHandlingJob:
    def __int__(self):
        pass

    def request_handling_flow(self):
        email_cleint_self = EmailClient().unread_mail_check_job_card()
        if email_cleint_self.get_message_loaded_status():
            email_message = email_cleint_self.get_email_message()
            for message in email_message:
                recipients = email_cleint_self.get_recipients(message)
                print(recipients)
                sender = recipients['From']
                email_sender_validation = SenderValidation().setparameters(sender=sender).senderisvalid()
                if email_sender_validation:
                    NotificationInsert().insert_details(sender,'request received, will validate your request and update you')
                    msg_list= email_cleint_self.message_walk(message)
                    ReportsRequest().reports_details(recipients,msg_list)
                    NotificationInsert().insert_details(sender,'Reports request created')
        else:
            print('Unread Message Not loaded')
        email_cleint_self.logout()
        print('This is coming from RequestHandling thread --> request handling flow')



if __name__ == '__main__':
    RequestHandlingJob().request_handling_flow()