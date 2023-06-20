import logging
import sys
import colorlog
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

#
#
# Ravikumar , June 14,2023
#
# code referred from many sites and  implemented my own. 
#

class logdetails:
    def __init__(self) -> None:
        pass

    def loginit(self,logpath):
        self.logger = logging.getLogger(__name__)
        stdout = colorlog.StreamHandler(stream=sys.stdout)
        fileHandler = RotatingFileHandler(logpath, backupCount=5, maxBytes=50000)



        fmt = jsonlogger.JsonFormatter(
            "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
            rename_fields={"levelname": "severity", "asctime": "timestamp"},
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        )


        stdout.setFormatter(fmt)
        fileHandler.setFormatter(fmt)

        self.logger.addHandler(stdout)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)

        return self

    def loggingdetails(self,level, msg , username,sessionid):
        if level == 'info':
            self.logger.info(msg, extra={"user": username, "session_id": sessionid})
        if level == 'warning':
            self.logger.warning(msg, extra={"user": username, "session_id": sessionid})
        if level == 'error':
            self.logger.error(msg, extra={"user": username, "session_id": sessionid})

if __name__ =='__main__':
    logdetails().loginit("Z_logs/logs.txt").loggingdetails('info',"Info message","johndoe","abc123")

