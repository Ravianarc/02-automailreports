#!/usr/bin/python
import os
from configparser import ConfigParser
from pathlib import Path,PurePath

#
#
# Ravikumar , June 14,2023
#
# code referred from many sites and  implemented my own. 
#

SECTION ='postgresql'
path = PurePath(os.getcwd())
fullpath = path.joinpath('common_configurations/database.ini')


class DatabaseInit:
    def __init__(self) -> None:
        pass

    def set_params(self):
        self.filename = fullpath
        self.section = SECTION
        return self


    def config(self):
        # create a parser
        parser = ConfigParser()
        parser.read(self.filename )
        # get section, default to postgresql
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))
        return db


def main():
    SECTION ='postgresql'
    path = PurePath(os.getcwd()).parent
    fullpath = path.joinpath('common_configurations/database.ini')
    print(fullpath)
    db = DatabaseInit().set_params().config()
    print(db)



if __name__ =="__main__":
    main()