#!/usr/bin/python
import os
import sys
import subprocess
#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#

#
# This class contains package install function and list all the installed packages
#
class packageinstall:
    def __init__(self,path,requirementFileName) -> None:
        self.path =path
        self.requirementFileName = requirementFileName
    

    #
    # Given package list in requirement.txt will be installed
    # in current python installation or virtual environment
    #
    def installpackages(self) -> bool:
        flag = True
        fullpath = self.path +'/InfastructureasCode/' + self.requirementFileName
        is_fileavailable = os.path.exists(fullpath)
        if is_fileavailable:

            with open(fullpath) as f:
                for line in f.readlines():
                    packagedetails =None
                    packagedetails = [sys.executable,'-m', 'pip', 'install',line]
                    subprocess.check_call(packagedetails)
        else:
            print('requirement file not available root path')
            flag = False
        
        return flag
    

    #
    # Retrun all the installed packages list
    #
    def getinstalledpackages(self) -> list:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        return installed_packages
            

#
# This is main function. This function created just for testing this class
#
def main():
    path=os.getcwd()
    requirementFileName = 'requirements.txt'
    status = packageinstall(path,requirementFileName).installpackages()
    if (status):
        print('sucessfully installed')
    else:
        print('some issue , please check mannually ')

    installed_packages = packageinstall(path,requirementFileName).getinstalledpackages()

    for packagename in installed_packages:
        print(packagename)



if __name__ =='__main__':
    main()