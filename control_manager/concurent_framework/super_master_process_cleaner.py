import datetime
import os
import signal
import sys

import pandas as pd

#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#


# Setting dynamic path to import projectlibs modules
# this can be avoid by  os.env[$path] or manual os environment path setting
# Please set this path in system environment to avoid some technical issue

lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)

channel_environment_path = os.getcwd() + '/' + 'communication_channel'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)


from communication_channel.concurentFrameWork.super_master_process_handler import ComponentMaster


class ProcessClean:
    def __init__(self) -> None:
        mydate = datetime.datetime.now() - datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")

    def check_pid(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


    def kill_process_by_name_of_service(self,service_name,clean_from_restart=False):
        try:
            process_id = ComponentMaster().get_process_id_by_service_name(service_name)
            if self.check_pid(process_id):
                self.kill_this_process(process_id,clean_from_restart=clean_from_restart)
        except Exception as e:
            print(f'caught {type(e)}: {e}')
        finally:
            print('finally executed')

    def kill_all_non_live_processes_and_clean(self):
        pf: pd.DataFrame = None
        try:
            pf = ComponentMaster().fetch_inactive_master_process()
            print('Number of inactive Process', pf)
            if pf is not None:
                for i in pf['processpid']:
                    if self.check_pid(i):
                        # if active
                        pass
                    else:
                        # If not active then only clean up from master table
                        ComponentMaster().clean_inactive_prorcess_in_master_by_id(str(i))

            pf: pd.DataFrame = None
            pf = ComponentMaster().fetch_master_process()
            print('Number of active Process', pf)
            if pf is not None:
                for i in pf['processpid']:
                    if self.check_pid(i):
                        # if active
                        pass
                    else:
                        # If not active then only clean up from master table
                        ComponentMaster().clean_inactive_prorcess_in_master_by_id(str(i))

        except Exception as e:
            print(f'caught {type(e)}: e')
        finally:
            print('finally executed')

    # Just kill the child process.
    # and put child in inactive
    def kill_this_process(self, process_id, update_status=False, clean_status=True,clean_from_restart=False):
        try:
            os.kill(process_id, signal.SIGKILL)
        except Exception as e:
            print(f'caught {type(e)}: {e}')
            raise e
        finally:
            print('finally executed in kill process')
            if update_status:
                ComponentMaster().update_master_active_status(str(process_id), 0)
                print('updated the status in Register')
            elif clean_status:
                ComponentMaster().clean_inactive_prorcess_in_master_by_id(str(process_id))
            elif clean_from_restart:
                ComponentMaster().remove_killed_sevice_from_restart_tocken(str(process_id))
            else:
                pass


    def kill_all_inactive_processind(self):
        try:
            pd = ComponentMaster().fetch_inactive_master_process()
            for i in pd['processpid']:
                self.kill_this_process(i, True)
        except Exception as e:
            print(f'caught {type(e)}: e')
            exit(1)
        finally:
            print('finally executed')


    def kill_all_process(self, includingParent=False):
        pf: pd.DataFrame = None
        try:
            pf = ComponentMaster().fetch_inactive_master_process()
            for i in pf['processpid']:
                self.kill_this_process(i, True)

            pf = ComponentMaster().fetch_master_process()
            for i in pf['processpid']:
                self.kill_this_process(i, True)

        except Exception as e:
            print(f'caught {type(e)}: e')
            exit(1)
        finally:
            print('finally executed')


if __name__ == "__main__":
    ProcessClean().kill_all_non_live_processes_and_clean()

