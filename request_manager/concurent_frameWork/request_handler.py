
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
lib_environment_path: str = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)


# setting envirionment path
channel_environment_path: str = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)


# setting envirionment path
control_environment_path:str = os.getcwd() + '/' + 'control_manager/concurent_framework'
if control_environment_path not in sys.path:
    sys.path.append(control_environment_path)

# setting envirionment path
jobs_environment_path:str = os.getcwd() + '/' + 'request_manager/product_job_controls'
if jobs_environment_path not in sys.path:
    sys.path.append(jobs_environment_path)

print(jobs_environment_path)
#Importing headbeat line from communicationchannel
# This is for process master registration. This can be remove as this is usefull for testing alone.
from super_master_process_handler import ComponentMaster
from request_send_tocken_to_lifeline import RequestSignalToken
from request_handling_job import RequestHandlingJob

#
#Heartbeat thread. every 5 minuts, this will update the life live extension
#
class Send_Token_to_lifeline(Thread):
    def __init__(self, processid,processname):
        Thread.__init__(self)
        self.processid = processid
        self.processname = processname
        self.registerby = 'requesthandler'

    def run(self):
        try :
            while True:
                RequestSignalToken().send_request_signal_token(self.processid,self.processname,self.registerby)
                sleep(5)
        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)


class RequestHandling(Thread):
    def run(self):
        try:
            while True:
                sleep(10)
                print('This is coming from RequestHandling thread')
                RequestHandlingJob().request_handling_flow()
        except Exception as e:
            print(f'caught {type(e)}: {e}')
            sys.exit(1)



class RequestHandler(Process):
    def __init__(self,name):
        Process.__init__(self)
        self.name =name
        self.signal_to_life_thread:Thread =None
        self.request_handling_thread:Thread = None

    def run(self):
        try :
            if self.signal_to_life_thread == None :
                self.signal_to_life_thread = Send_Token_to_lifeline(self.pid,self.name)
                self.signal_to_life_thread.start()

            if self.request_handling_thread == None:
                self.request_handling_thread = RequestHandling()
                self.request_handling_thread.start()

            self.signal_to_life_thread.join()
            self.request_handling_thread.join()
        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)



if __name__ == '__main__':
    request_process = RequestHandler(name='requesthandler')
    request_process.start()
    print('From Parent , the child process id ',request_process.pid)
    print('From Parent , the child process id ',request_process.name)
    ComponentMaster().master_register(request_process.pid, request_process.name)
    request_process.join()

