#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#

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


class ReportsRequest:
    def __init__(self) -> None:
        self.sender = None
        self.receiver = None
        self.cc =None
        self.bcc = None
        self.reportname =None
        self.params =None
        self.type=None
        self.query=None

    def reports_details(self,recipients,msg_list):
        cc =None
        bcc = None
        params =None
        type=None
        query=None
        system = None

        for key in recipients.keys():
            match key:
                case 'From': sender =recipients[key]
                case 'To': receiver = recipients[key]
                case 'Cc': cc = recipients[key]
                case 'Bcc': bcc = recipients[key]
                case _ : print('No input')
        ## Need to check , report name should not be empty
        for msg in msg_list:
            report_msg_part = msg.split(':')
            match report_msg_part[0].strip().lower():
                case 'reportname' : reportname = report_msg_part[1].strip()
                case 'parameter' : params = report_msg_part[1].strip()
                case 'type' : type = report_msg_part[1].strip()
                case 'query' : query = report_msg_part[1].strip()
                case 'system' : system = report_msg_part[1].strip()
        self.query_parameters(sender,receiver,cc,bcc,reportname,params,type,query,system)
        self.reports_details_insert()
        # get the request id and send to user notification for reference


    def query_parameters(self,sender,receiver,cc,bcc,reportname,params,type,query,system):
        self.sender = sender
        self.receiver = receiver
        self.cc =cc
        self.bcc = bcc
        self.reportname =reportname
        self.params =params
        self.type=type
        self.query=query
        self.system = system
        return self


    def query_preparation(self):
        query = '''insert into public.reports_request_info (
        report_name, parameters, sender, cc, bcc, type_of_report, report_query, reporting_system, validation_status) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        return query


    def reports_details_insert(self):
        connection =None
        try:
            sql = self.query_preparation()
            tuples = (self.reportname,self.params,self.sender,self.cc,self.bcc,self.type,self.query,self.system,0)
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql,tuples)
            connection.commit()
            connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


    def get_report_id(self):
        connection =None
        try:
            sql = 'select id from reports_request_info where report_name =\''+self.reportname+ '\''\
                  'and  parameters =\'' + self.params + '\''\
                    'and  sender = \'' + self.sender + '\'' \
                    'and  type_of_report =\'' + self.type + '\''\
                    'and reporting_system =\'' + self.system +'\'' \
                    'and  validation_status = \'0\';'
            print(sql)
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            connection.close()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

if __name__=='__main__':

    recipients = {'From': 'manovairavi@hotmail.com', 'To': 'ravianarc@outlook.com'}
    msg_list =['Reportname : test', 'parameter : { fromdate = 153 , twodate=456}', 'type:existing','query:select * from table where id="2"','system:sample']
    ReportsRequest().reports_details(recipients,msg_list)
    #emailsendervalidation.putrecordsintemplocation()



