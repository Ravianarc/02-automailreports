from typing import Any
from multiprocessing import Process
from threading import Thread
from time import sleep
import sys
import os
import datetime

#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#

# setting envirionment path
channel_environment_path = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)

print(channel_environment_path)
# print(channel_environment_path)
from services_life_extender_line import ServiceLifeExtender


class LifelineManager(Process):
    def __init__(self, name):
        Process.__init__(self)
        self.name = name

    def run(self):
        try:
            # while True:
            time_now = datetime.datetime.now()
            process_details = ServiceLifeExtender().fetch_active_process()
            for process in process_details:
                process_id = process[0]
                services = process[1]
                process_extenting_process_life_time = process[5]
                match services:
                    case "NotifyManager":
                        difference = time_now - process_extenting_process_life_time
                        duration_in_s = difference.total_seconds()
                        diff_in_minutes = divmod(duration_in_s, 60)[0]
                        if diff_in_minutes > 10:
                            ServiceLifeExtender().put_service_restart_tokens(process_id, services, 1)
                            print(services, ' need to be restarted : not reaching to life line for the minuts of ',
                                  diff_in_minutes)
                            ServiceLifeExtender().remove_active_process_by_id(process_id)
                            print(services, ':deleted from monitoring list ')

                    case "DispatchManager":
                        difference = time_now - process_extenting_process_life_time
                        duration_in_s = difference.total_seconds()
                        diff_in_minutes = divmod(duration_in_s, 60)[0]
                        if diff_in_minutes > 10:
                            ServiceLifeExtender().put_service_restart_tokens(process_id, services, 1)
                            print(services, ' need to be restarted : not reaching to life line for the minuts of ',
                                  diff_in_minutes)
                            ServiceLifeExtender().remove_active_process_by_id(process_id)
                            print(services, ':deleted from monitoring list ')

                    case "ReportingManager":
                        difference = time_now - process_extenting_process_life_time
                        duration_in_s = difference.total_seconds()
                        diff_in_minutes = divmod(duration_in_s, 60)[0]
                        if diff_in_minutes > 10:
                            ServiceLifeExtender().put_service_restart_tokens(process_id, services, 1)
                            print(services, ' need to be restarted : not reaching to life line for the minuts of ',
                                  diff_in_minutes)
                            ServiceLifeExtender().remove_active_process_by_id(process_id)
                            print(services, ':deleted from monitoring list ')

                    case "RequestManager":
                        difference = time_now - process_extenting_process_life_time
                        duration_in_s = difference.total_seconds()
                        diff_in_minutes = divmod(duration_in_s, 60)[0]
                        if diff_in_minutes > 10:
                            ServiceLifeExtender().put_service_restart_tokens(process_id, services, 1)
                            print(services, ' need to be restarted : not reaching to life line for the minuts of ',
                                  diff_in_minutes)
                            ServiceLifeExtender().remove_active_process_by_id(process_id)
                            print(services, ':deleted from monitoring list ')
                    case _:
                        print('Need to add this service in process handler:', services)


        except Exception as e:
            print(f'caught {type(e)}: e')
            sys.exit(1)


if __name__ == '__main__':
    process = LifelineManager(name='LifelineManager')
    process.start()

