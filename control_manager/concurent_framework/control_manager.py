import os
import sys

#
#
# Ravikumar Vaithilingam (RV), June 14,2023
# code referred / studied from many sites /books and  implemented my own.
#

# setting envirionment path
lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)

# setting envirionment path
channel_environment_path = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)

# Getting service name to call
from communication_channel.concurentFrameWork.super_master_process_handler import ComponentMaster
from super_master_process_cleaner import ProcessClean

from process_handler import ProcessHandler
from lifeline_manager import LifelineManager


# Getting ready to start the services based the service registered tokens
class ControlManager:
    def __init__(self, name):
        self.name = name

    def start_services(self):
        try:
            ProcessClean().kill_all_non_live_processes_and_clean()
            service_registered_tokens = ComponentMaster().get_service_registered_tokens()
            process_handler = ProcessHandler(name='ProcessHandler',service_registered_tokens=service_registered_tokens)
            process_handler.start()


            life_line_manager = LifelineManager(name='LifelineManager')
            life_line_manager.start()

            ComponentMaster().master_register(process_handler.pid, process_handler.name)
            ComponentMaster().master_register(life_line_manager.pid, life_line_manager.name)

            process_handler.join()
            life_line_manager.join()

        except Exception as error:
            print(error)


if __name__ == '__main__':
    process = ControlManager(name='controlManager')
    process.start_services()
