#!/usr/bin/python
import os
#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#

#
# Projects folders creations
#
class projectfolders:
    def __init__(self,path,folderlist) -> None:
        self.path =path
        self.folderlist = folderlist
    
    def createfloders(self) -> bool:
        flag = True
        for foldername in self.folderlist:
            fullpath = self.path +'/' + foldername
            if not os.path.exists(fullpath):
                os.mkdir(fullpath)
            else:
                flag = False
        
        return flag
            


def main():
    path=os.getcwd()
    listfolders:list = ['analytics','api','conf','docs','Iac','jobs','ml','orches','pipelines','projectlibs','stream','viz']
    status = projectfolders(path,listfolders).createfloders()
    if (status):
        print('sucessfully created all the folders')
    else:
        print('Some folders or all folders are already created')



if __name__ =='__main__':
    main()