import datetime
import os
import sys

import pandas as pd
import psycopg2

#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#
# have two table: 
# processActiveRegister - This will have only active processes
# processMasterRegister - All the process that created by controller and no active process will be cleaned
#


# Setting dynamic path to import projectlibs modules
# this can be avoid by  os.env[$path] or manual os environment path setting
# Please set this path in system environment to avoid some technical issue

lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)

# importing project libs modules
from storage_connection import connect, sql_alchemy_connection


# Each methods will work individual ,Becuase , if we put in docker container for scale up ,it will be usefull
class ComponentMaster:
    def __init__(self) -> None:
        mydate = datetime.datetime.now() - datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")

    #### Master Process
    #
    # Registering the process details in master. Thes is exceptional process action
    # For now , I am using dB. But can be used in-memore or query or etc.
    #
    def master_register(self, processid, processname):
        connection = None
        try:
            mydatetime = datetime.datetime.now()
            record_to_insert = [processid, processname, 1, mydatetime, 1]
            data = {
                "processpid": record_to_insert[0]
                , "processname": record_to_insert[1]
                , "processstatus": record_to_insert[2]
                , "processcreationtime": record_to_insert[3]
                , "processactiveind": record_to_insert[4]
            }
            df = pd.DataFrame(data, index=[1])
            with sql_alchemy_connection() as connection:
                done = df.to_sql('processMasterRegister', con=connection, if_exists='append', index=False)
            #print('Number of rows insert', done)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    #
    # Update the status. in master register for exception kill cause
    #
    def clean_inactive_prorcess_in_master_by_id(self, processid):
        connection = None
        try:
            sql = f"DELETE FROM  \"processMasterRegister\"  WHERE processpid = " + processid + ";"
            print(sql)
            with connect() as connection:
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    #
    # Update the status. in master register for exception kill cause
    #
    def clean_inactive_prorcess_in_master(self):
        connection = None
        mydatetime = datetime.datetime.now()
        try:
            sql = f""" DELETE FROM  "processMasterRegister"  WHERE processactiveind = '0'"""
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

                #

    # Update the status. in master register for exception kill cause
    #
    def update_master_active_status(self, processid, activestatus):
        connection = None
        mydatetime = datetime.datetime.now()
        try:
            sql = f""" UPDATE "processMasterRegister"  SET processactiveind = %s   WHERE processpid = %s"""
            with connect() as connection:
                cursor = connection.cursor()
                cursor.execute(sql, (activestatus, processid))
                connection.commit()
                connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

            #

    # getting all the masterregister process
    #
    def fetch_inactive_master_process(self):
        pf: pd.DataFrame = None
        connection = None
        columnsName = ['processpid']
        try:
            sql1 = '''select processpid from "processMasterRegister" where processactiveind = 0;'''

            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()

            index_list = []
            for i in range(len(data)):
                index_list.append(i + 1)
            df = pd.DataFrame(data, index=index_list, columns=columnsName)
            return df
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    #
    # getting all the masterregister process
    #
    def fetch_master_process(self):
        pf: pd.DataFrame = None
        connection = None
        columnsName = ['processpid']
        try:
            sql1 = '''select processpid from "processMasterRegister" where processactiveind = 1;'''
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            index_list = []
            for i in range(len(data)):
                index_list.append(i + 1)
            df = pd.DataFrame(data, index=index_list, columns=columnsName)
            return df
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    #
    # Display the content
    #
    def display_master(self):
        connection = None
        try:
            with connect() as connection:
                cursor = connection.cursor()
                sql1 = '''select * from "processMasterRegister" where processactiveind = 1;'''
                cursor.execute(sql1)
                for i in cursor.fetchall():
                    print(i)
                connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()



    def get_process_id_by_service_name(self,service_name):
        process_id = None
        connection = None
        try:
            sql1 = '''select processpid from "processMasterRegister" where processname = %s;'''
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1,(service_name))
            data = cursor.fetchall()
            connection.close()
            for row in data:
                process_id = [row[0]]
            return process_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


#----------------------------------------------------------------------------#

    def remove_killed_sevice_from_restart_tocken(self, service_id):
        connection = None
        try:
            sql = f"DELETE FROM  \"ServiceRestart\"  WHERE serviceid = " + service_id + ";"
            print(sql)
            with connect() as connection:
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_service_registered_tokens(self):
        service_tokens = {}
        connection = None
        try:
            sql1 = '''select servicename , registerind from "ServiceRegister" ;'''
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            for row in data:
                service_tokens[row[0]] = row[1]
            return service_tokens
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def get_service_restart_tokens(self):
        service_restart_tokens = {}
        connection = None
        try:
            sql1 = '''select serviceid , servicename , restartind  from "ServiceRestart" where restartind = 1;'''
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            for row in data:
                service_restart_tokens[row[0]] = row[1]
            return service_restart_tokens
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


if __name__ == '__main__':
    print(os.getcwd())
    #df = ComponentMaster().get_service_registered_tokens()
    df = ComponentMaster().get_service_restart_tokens()
    #df = ComponentMaster().display_master()
    print(df)
