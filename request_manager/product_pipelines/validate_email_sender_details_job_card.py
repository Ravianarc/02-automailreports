#!/usr/bin/python
import datetime
import os
import sys
import psycopg2

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

# importing project libs modules
from storage_connection import connect, sql_alchemy_connection



class SenderValidation:
    def __init__(self) -> None:
        self.sender = None


    def setparameters(self,sender):
        self.sender = sender
        return self


    def senderisvalid(self) -> bool:
        connection = None
        status = None
        try:
            sql1 = 'SELECT is_valid FROM public.mail_users  where is_valid = \'1\' and user_email_id=\''+self.sender+'\''
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql1)
            data = cursor.fetchall()
            connection.close()
            if len(data) > 0 :
                status = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
            if status:
                return True
            else:
                return False


if __name__=='__main__':
    sender ='sender@gmail.com'
    receiver ='receiver@outlook.com'
    cced ='cced@hotmail.com'
    ReportName ='Healthcare-monthly-report'
    params ={"fromDate":"","todate":"" }

    emailsendervalidation = SenderValidation().setparameters(sender=sender).isvalid()
    print(emailsendervalidation)
    #emailsendervalidation.putrecordsintemplocation()

    