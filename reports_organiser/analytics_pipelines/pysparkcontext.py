import os,sys
from typing import Any, Dict, Optional

#os.environ["PYSPARK_PYTHON"] = "/home/rv/projects/automailreports/automailreports/bin/python"
#os.environ["SPARK_HOME"] = "/home/rv/projects/automailreports/automailreports/lib/python3.10/site-packages"
#os.environ["PYLIB"] = os.environ["SPARK_HOME"] + "/python/lib"
#sys.path.insert(0, os.environ["PYLIB"] +"/py4j-0.9-src.zip")
#sys.path.insert(0, os.environ["PYLIB"] +"/pyspark.zip")


import findspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
findspark.init()



class pysparksession():
    def __init__(self,name):
        self.name = name


    def getEntrypoint(self):
        spark = (SparkSession
         .builder
         .appName("Analyzing the vocabulary of Pride and Prejudice.")
         .getOrCreate())
        
        spark.sparkContext.setLogLevel("INFO")
        print(spark.version)

    


if __name__ =='__main__':
    pysparksession('Analyzing').getEntrypoint()