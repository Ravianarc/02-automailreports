from multiprocessing import Process
import datetime
from time import sleep

from communication_channel.concurentFrameWork.super_master_process_handler import ComponentMaster
from super_master_process_cleaner import ProcessClean
#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#




class ProcessHandler(Process):
    def __init__(self, name,service_registered_tokens):
        Process.__init__(self)
        mydate = datetime.datetime.now() - datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
        self.name = name
        self.service_registered_tokens = service_registered_tokens
        self.notification_manager_service_token = 0
        self.dispatching_manager_service_token = 0
        self.reporting_manager_service_token = 0
        self.requesting_manager_service_token = 0

        self.notification_manager_service_restart_token = 0
        self.dispatching_manager_service_restart_token = 0
        self.reporting_manager_service_restart_token = 0
        self.requesting_manager_service_restart_token =0

        self.NotifyManager: Process = None
        self.DispatchManager: Process = None
        self.ReportingManager: Process = None
        self.RequestManager: Process = None


    def run(self):
        try:
            # Getting token for service registeration. If registered and set to process, the process will be started
            for services in self.service_registered_tokens.keys():
                match services:
                    case "NotifyManager":
                        self.notification_manager_service_token = self.service_registered_tokens.get(services)
                    case "DispatchManager":
                        self.dispatching_manager_service_token = self.service_registered_tokens.get(services)
                    case "ReportingManager":
                        self.reporting_manager_service_token = self.service_registered_tokens.get(services)
                    case "RequestManager":
                        self.requesting_manager_service_token = self.service_registered_tokens.get(services)
                    case _:
                        print('Need to add this service in process handler')

            # Every 5 minuts loop will check the health of process and will make decisions
            # while True:
            # if any  supervisor advice to restart , due to service upgrade or update.
            # if lifeline Manager advice for restart , due to service is out of contorl as service is not sending heartbeat

            self.get_service_restart_tokens = ComponentMaster().get_service_restart_tokens()

            #Reset the service restart token , if it is processed already

            self.notification_manager_service_restart_token = 0
            self.dispatching_manager_service_restart_token = 0
            self.reporting_manager_service_restart_token = 0
            self.requesting_manager_service_restart_token =0

            for services in self.get_service_restart_tokens.keys():
                match services:
                    case "NotifyManager":
                        self.notification_manager_service_restart_token = self.get_service_restart_tokens.get(services)
                    case "DispatchManager":
                        self.dispatching_manager_service_restart_token = self.get_service_restart_tokens.get(services)
                    case "ReportingManager":
                        self.reporting_manager_service_restart_token = self.get_service_restart_tokens.get(services)
                    case "RequestManager":
                        self.requesting_manager_service_restart_token = self.get_service_restart_tokens.get(services)
                    case _:
                        print('No Restart Token...')


            if self.notification_manager_service_token and self.notification_manager_service_restart_token:
                ProcessClean().kill_process_by_name_of_service('NotifyManager',clean_from_restart=True)
                print('Killing')

            if self.dispatching_manager_service_token and self.dispatching_manager_service_restart_token:
                ProcessClean().kill_process_by_name_of_service('DispatchManager',clean_from_restart=True)
                print('Killing')

            if self.reporting_manager_service_token and self.reporting_manager_service_restart_token:
                ProcessClean().kill_process_by_name_of_service('ReportingManager',clean_from_restart=True)
                print('Killing')

            if self.requesting_manager_service_token and self.requesting_manager_service_restart_token:
                ProcessClean().kill_process_by_name_of_service('RequestManager',clean_from_restart=True)
                print('Killing')


            # service token set from control manager
            if self.notification_manager_service_token:
                time_now = datetime.datetime.now()
                if (self.NotifyManager is not None) and (self.NotifyManager.is_alive()):
                    print('NotifyManager is alive at the time :',time_now)
                else:
                    print('NotifyManager is not alive at the time :',time_now)
                    print('Starting NotifyManager ...',time_now)
                    #Starting call
                    sleep(5)
                    print('Process Registered with Master list ...',time_now)


            if self.dispatching_manager_service_token:
                time_now = datetime.datetime.now()
                if (self.DispatchManager is not None) and (self.DispatchManager.is_alive()):
                    print('DispatchManager is alive at the time :',time_now)
                else:
                    print('DispatchManager is not alive at the time :',time_now)


            if self.reporting_manager_service_token:
                time_now = datetime.datetime.now()
                if (self.ReportingManager is not None) and (self.ReportingManager.is_alive()):
                    print('ReportingManager is alive at the time :',time_now)
                else:
                    print('ReportingManager is not alive at the time :',time_now)
                    print('Starting ReportingManager ...',time_now)
                    #Starting call
                    print('Process Registered with Master list ...',time_now)


            if self.requesting_manager_service_token:
                time_now = datetime.datetime.now()
                if (self.RequestManager is not None) and (self.RequestManager.is_alive()):
                    print('RequestManager is alive at the time :',time_now)
                else:
                    print('RequestManager is not alive at the time :',time_now)
                    print('Starting RequestManager ...',time_now)
                    #Starting call
                    print('Process Registered with Master list ...',time_now)



        except Exception as e:
            print(f'caught {type(e)}: {e}')






if __name__ == '__main__':
    print('')
    #process = controlManager(name='controlManager')
    #process.start()
    #print('From Parent , the child process id ',process.pid)
    #print('From Parent , the child process id ',process.name)
    #componentbeat().masterRegister(process.pid,process.name)
    #process.join()
    #print(process.exitcode)