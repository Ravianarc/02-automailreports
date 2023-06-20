import os
import sys
import psycopg2

# setting envirionment path
lib_environment_path = os.getcwd() + '/' + 'common_project_libs'
if lib_environment_path not in sys.path:
    sys.path.append(lib_environment_path)


# importing project libs modules
from storage_connection import connect, sql_alchemy_connection


class ReportAuthorityValidation:
    def __init__(self):
        pass

    def validation_check(self,report_id,sender,report_type,source_system=None):
        connection = None
        status = None
        if report_type==('existing'):

            sql1 = 'SELECT 1  FROM public.report_permission where report_id=\''+ str(report_id) \
                    + '\' and  user_mail_id=\''+sender+'\' and active = 1'
        else:
            sql1 = 'SELECT 1  FROM public.source_permission where report_name=\''+ source_system \
                   + '\' and  user_mail_id=\''+sender+'\' and active = 1'
        try:
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


if __name__ == '__main__':
    isvalid = ReportAuthorityValidation().validation_check(1,'manovairavi@hotmail.com','existing')
    print(isvalid)