import os
import sys
import datetime
import psycopg2
import pandas as pd


#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites / books and  implemented my own. 
# Also this is for study purpose.
#
# This is one of the communication channel line . 
# Thought is , if you put mail address and details , it will be notified to corresponding address.
# All the product part can send notification to this line. 
# Notification manager will read this message and send to address.
#

# setting envirionment path
lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)


# importing project libs modules
from storage_connection import connect, sql_alchemy_connection


#Each methods will work individual ,Becuase , if we put in docker container for scale up ,it will be usefull
class LogicDetailsSharing:
    def __init__(self) -> None:
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")

    #
    # Inserting the notification details to channel storage
    # For now , I am using dB. But can be used in-memore or query or etc.
    # Now using pandas for insert , as it is easy for me. Implement here, if you have better approach.
    #
    def insert_reprot_request_details(self,emailid,details):
        connection = None
        try:
            mydatetime = datetime.datetime.now()
            mydefaultdatetime = datetime.datetime(1900,1,1,00,00,00,000000)
            record_to_insert = [emailid, details, 0 ,mydatetime,mydefaultdatetime]
            data={
                "notifyemailaddress": record_to_insert[0]     
                ,"notifydetails": record_to_insert[1]    
                ,"notifystatus": record_to_insert[2]
                ,"notifycreationtime":record_to_insert[3]
                ,"notifysenttime" :record_to_insert[4]
            }
            df = pd.DataFrame(data,index=[1])
            connection = sql_alchemy_connection()
            df.to_sql('notification', con=connection, if_exists='append',index=False)
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                    connection.close()


    #
    # Update the status. O
    # once notification sent , need to update the status of notification message as not need process again.
    #
    def update_report_request_status(self,notifyid,notifystatus):
        connection = None
        mydatetime = datetime.datetime.now()
        try:
            sql = f""" UPDATE notification
                    SET notifystatus = %s
                    ,notifysenttime = %s
                    WHERE notifyid = %s"""
            print(sql,(notifystatus, mydatetime ,notifyid))
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql, (notifystatus, mydatetime ,notifyid))     
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                    connection.close()
    #
    # getting all the unprocessed notification for processing
    # Only non processed notifications need to send
    #
    def fetch_unprocessed_report_request(self,validation_status=0):
        connection = None
        columnsName =['id', 'report_name', 'parameters', 'sender','cc','bcc'
            ,'type_of_report','report_query','reporting_system','validation_status']
        try:
            connection = connect()
            cursor = connection.cursor()
            sql1 = 'select * from reports_request_info where validation_status =\''+ validation_status +'\';'
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            index_list =[]
            for i in range(len(data)):
                index_list.append(i+1)
            df = pd.DataFrame(data,index=index_list)
            df.columns =columnsName
            return df
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                    connection.close()

    #
    # Display the content
    # this is for testing query
    #
    def display(self):
        connection = None
        try:
            connection = connect()
            cursor = connection.cursor()
            sql1 = '''select * from reports_request_info ;'''
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            for i in data:
                print(i)

        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        finally:
                if connection is not None:
                    connection.close()


if __name__ =='__main__':
    #notificationinsert().insertdetails(emailid='xyz@gamil.com',details='Ready to test')
    #notificationinsert().updatestatus(notifyid=1,notifystatus=1)
    #notificationinsert().display()
    df =LogicDetailsSharing().fetch_unprocessed_report_request(validation_status='0')
    print(df.columns)

