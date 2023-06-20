
from typing import Any
from multiprocessing import Process
from threading import Thread
from time import sleep
import sys 
import os

#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#


#Setting dynamic path to import projectlibs modules
#this can be avoid by  os.env[$path] or manual os environment path setting
#Please set this path in system environment to avoid some technical issue

# setting envirionment path
lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)

# setting envirionment path
channel_environment_path = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)

# setting envirionment path
notification_environment_path = os.getcwd() + '/' + 'notification_manager/concurent_frameWork'
if notification_environment_path not in sys.path:
    sys.path.append(notification_environment_path)

# setting envirionment path
control_environment_path = os.getcwd() + '/' + 'control_manager/concurent_framework'
if control_environment_path not in sys.path:
    sys.path.append(control_environment_path)


#Importing headbeat line from communicationchannel
# This is for process master registration. This can be remove as this is usefull for testing alone.
from super_master_process_handler import ComponentMaster
from notify_send_tocken_to_lifeline import NotificationSignalToken

#
#Heartbeat thread. every 5 minuts, this will update the life live extension
#
class Send_Token_to_lifeline(Thread):
    def __init__(self, processid,processname):
            Thread.__init__(self)
            self.processid = processid
            self.processname = processname
            self.registerby = 'notificationhandler'

    def run(self):
        try :
            while True:
                NotificationSignalToken().send_notification_signal_token(self.processid,self.processname,self.registerby)
                sleep(5)
        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)


class NotifiocationSend(Thread):
    def run(self):
        try:
            while True:
                sleep(10)
                print('This is coming from NotifiocationSend thread')
        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)



class NotificationHandler(Process):
    def __init__(self,name):
        Process.__init__(self)
        self.name =name
        self.signal_to_life_thread:Thread =None
        self.notifiocation_thread:Thread = None

    def run(self):
        try :
            if self.signal_to_life_thread == None :
                self.signal_to_life_thread = Send_Token_to_lifeline(self.pid,self.name)
                self.signal_to_life_thread.start()

            if self.notifiocation_thread == None:
                self.notifiocation_thread = NotifiocationSend()
                self.notifiocation_thread.start()

            self.signal_to_life_thread.join()
            self.notifiocation_thread.join()
        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)



if __name__ == '__main__':
    notification_process = NotificationHandler(name='NotificationHandler')
    notification_process.start()
    print('From Parent , the child process id ',notification_process.pid)
    print('From Parent , the child process id ',notification_process.name)
    ComponentMaster().master_register(notification_process.pid, notification_process.name)
    notification_process.join()

