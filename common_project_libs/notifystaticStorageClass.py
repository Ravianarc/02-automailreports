
#!/usr/bin/python

#
#
# Ravikumar , June 14,2023
#
# code referred / studied from many sites /books and  implemented my own. 
#



#
#This class defined just for testing purpose . used as DB table
#
class notify:
    id:int = 0
    notification:list ={}

    @classmethod
    def insertvalue(cls,details,status):
        detailrecord = [details,status]
        cls.id += 1
        cls.notification[cls.id] = detailrecord

    @classmethod
    def display(cls):
        print('incremental id:', cls.id)
        print('details:',cls.notification)

if __name__ =='__main__':

    notify.insertvalue('ravi',0)
    notify.insertvalue('ravi',1)

    notify.display()