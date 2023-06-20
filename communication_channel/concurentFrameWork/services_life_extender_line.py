import os
import sys
import datetime
import psycopg2
import pandas as pd
from sqlalchemy import Connection


#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#
# 
# processActiveRegister - This will have only active processes
# extendmylife signal: first check the processed registered or not. If not , it will triger registerme signal.
# Next beat onwards , it will extend the process life. if it is not extendmylife signal passing then 
# controller may kill this component  and recreate another component instance.


# Setting dynamic path to import projectlibs modules
# this can be avoid by  os.env[$path] or manual os environment path setting
# Please set this path in system environment to avoid some technical issue

lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)

# importing project libs modules
from storage_connection import connect, sql_alchemy_connection


#Each methods will work individual ,Becuase , if we put in docker container for scale up ,it will be usefull
class ServiceLifeExtender:
    def __init__(self) -> None:
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
 
 #### Active Process 
    #
    # Display the content
    #
    def display_active_process(self):
        connection = None
        try:
            connection = connect()
            cursor = connection.cursor()
            sql1 = '''select * from processliferegister;'''
            cursor.execute(sql1)
            for i in cursor.fetchall():
                print(i)
            connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                    connection.close()

    def check_pid(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


    #This is only way to check process live or not
    def get_process_id_from_master(self,service_name):
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
    #
    # getting all the active life process
    #
    def fetch_active_process(self):
        df = None
        data =None
        connection = None
        try:
            connection = connect()
            cursor = connection.cursor()
            sql1 = '''select * from processliferegister ;'''
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                     connection.close()   

    #
    # getting all the active life process
    #
    def isactive_process_by_id(self,processid):
        connection = None
        try:
            data = None
            connection = connect()
            cursor = connection.cursor()
            sql1 = 'select * from processliferegister where processpid =\'' + processid +'\';'
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            if len(data) !=0:
                return True
            else:
                return False
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                     connection.close()


    def remove_active_process_by_id(self,processid):
        connection = None
        try:
            data = None
            connection = connect()
            cursor = connection.cursor()
            sql1 = f'delete from \"processliferegister\" where processpid =\'' + processid +'\';'
            cursor.execute(sql1)
            connection.commit()
            connection.close()
            return  True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


                # This is for lifeextension
    def register_me(self,processid,processname,registerby):
        connection = None
        try:
            mydatetime = datetime.datetime.now()
            mydefaultdatetime = datetime.datetime(1900,1,1,00,00,00,000000)
            record_to_insert = [processid, processname, 1 ,registerby,mydatetime,mydatetime]
            data={
                "processpid": record_to_insert[0]     
                ,"processname": record_to_insert[1]    
                ,"processstatus": record_to_insert[2]
                ,"processregisterby":record_to_insert[3]
                ,"processcreationtime" :record_to_insert[4]
                ,"extentingprocesslife" :record_to_insert[5]
            }
            df = pd.DataFrame(data,index=[1])
            connection = sql_alchemy_connection()
            df.to_sql('processliferegister', con=connection, if_exists='append',index=False)
            connection.close()
        except (Exception,psycopg2.DatabaseError) as error:
                raise error
        finally:
                print('registerme Final called')
                if connection is not None:
                     connection.close()
   

    #processlife extender
    def extendmy_life(self,processid,processname,registerby):
        connection = None
        try:
            sql = f""" UPDATE "processliferegister"
                    SET extentingprocesslife = %s
                    WHERE processpid = %s"""
            # Need to check if already registered or not. 
            # Based on the status , the process will be initiated
            if self.isactive_process_by_id(str(processid)):
                print('Process already registered')
                mydatetime = datetime.datetime.now()
                connection = connect()
                cursor = connection.cursor()
                cursor.execute(sql, (mydatetime ,str(processid)))     
                connection.commit()
                connection.close()    
            else:
                 print('Process already not registered')
                 self.register_me(processid,processname,registerby)
                 
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                print('extendmylife final called')
                if connection is not None:
                     connection.close()


    def put_service_restart_tokens(self,serviceid,servicename,restartind=1):
        connection = None
        try:
            record_to_insert = [serviceid, servicename,restartind]
            data={
                "serviceid": record_to_insert[0]
                ,"servicename": record_to_insert[1]
                ,"restartind": record_to_insert[2]
            }
            df = pd.DataFrame(data,index=[1])
            connection = sql_alchemy_connection()
            df.to_sql('ServiceRestart', con=connection, if_exists='append',index=False)
            connection.close()
        except (Exception,psycopg2.DatabaseError) as error:
            raise error
        finally:
            print('ServiceRestart Final called')
            if connection is not None:
                connection.close()


if __name__ =='__main__':
    ServiceLifeExtender().extendmy_life(processid=456,processname='NotifyManager' , registerby='ravi')
    #notificationinsert().updatestatus(notifyid=1,notifystatus=1)
    #notificationinsert().display()
    df = ServiceLifeExtender().fetch_active_process()
    print(df)
