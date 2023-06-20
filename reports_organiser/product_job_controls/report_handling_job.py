
import os
import sys

# setting envirionment path
pipelines_environment_path:str = os.getcwd() + '/' + 'reports_organiser/product_pipelines'
if pipelines_environment_path not in sys.path:
    sys.path.append(pipelines_environment_path)


# setting environment path
channel_environment_path:str = os.getcwd() + '/' + 'communication_channel/concurentFrameWork'
if channel_environment_path not in sys.path:
    sys.path.append(channel_environment_path)


from notification_line  import NotificationInsert
from logic_details_sharing_line import LogicDetailsSharing
from report_authority_validation import ReportAuthorityValidation

class ReportHandlingJob:
    def __init__(self):
        pass

    def report_handling_flow(self):
        step2 = False
        step3 = False
        step4 = False
        df =LogicDetailsSharing().fetch_unprocessed_report_request(validation_status='0')
        if len(df) > 0:
            report_list = (df.values.tolist())
            for report in report_list:
                #step 1: Call validation user permission check
                    # if yes - next step , Otherwise - Send notification
                has_permission = ReportAuthorityValidation().validation_check(report_id=report[0],sender=report[3] \
                                                                            ,report_type=report[6],source_system=report[8])
                if has_permission:
                        step2 = True

                else: NotificationInsert().insert_details(report[3],'User don\'t have permission for the reprot')

                #step 2: checking the report requirement with configuration
                if step2:
                    step3 = True

                #step 3: calling report generation
                if step3:
                    print()

                #change the status for dispatching
                if step4:
                    print()

    def assign_column_name(self):
        columnsName =['id', 'report_name', 'parameters', 'sender','cc','bcc'
            ,'type_of_report','report_query','reporting_system','validation_status']

if __name__ =='__main__':
    ReportHandlingJob().report_handling_flow()