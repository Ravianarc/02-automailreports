
import os,sys
import datetime

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
channel_environment_path = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)


#Importing headbeat line from communicationchannel
from services_life_extender_line import ServiceLifeExtender


class ReportSignalToken:
    def __init__(self) -> None:
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")

    def send_report_signal_token(self,processid,processname,registerby):
        try :
            ServiceLifeExtender().extendmy_life(processid,processname,registerby)
            print('request notification done')
        except Exception as e:
            print(f'caught {type(e)}: e')




if __name__ =='__main__':
    processid ='Test Process id'
    processname ='Test Process Name'
    registerby ='registerbynotificationself'
    ReportSignalToken().send_report_signal_token(processid,processname,registerby)