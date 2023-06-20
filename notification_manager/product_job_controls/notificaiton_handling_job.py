
import os
import sys
from pandas import DataFrame

# setting envirionment path
pipelines_environment_path:str = os.getcwd() + '/' + 'notification_manager/product_pipelines'
if pipelines_environment_path not in sys.path:
    sys.path.append(pipelines_environment_path)

# setting environment path
channel_environment_path:str = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)

print(pipelines_environment_path)

from notification_line  import NotificationInsert
from notifications_send import SentNotificationEmailClient

class NotificationHandlingJob:
    def __int__(self):
        df:DataFrame

    def notification_handling_flow(self):
        df = NotificationInsert().fetch_unprocessed_notifications()
        notificaiton_list = df.values.tolist()
        for notificaiton in notificaiton_list:
            print(notificaiton[0],(notificaiton[1]),(notificaiton[2]))
            SentNotificationEmailClient().send_notificaiton_job_card((notificaiton[2]),(notificaiton[1]))
            NotificationInsert().update_status(notificaiton[0],1)


if __name__ == '__main__':
    NotificationHandlingJob().notification_handling_flow()