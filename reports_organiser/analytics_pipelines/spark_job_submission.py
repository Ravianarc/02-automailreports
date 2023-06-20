import subprocess
#spark_submit_str= "spark-submit --master local[*] --deploy-mode cluster wordByExample.py"
spark_submit_str= "spark-submit --master local[*]  pysparkcontext.py"
process=subprocess.Popen(spark_submit_str,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
stdout,stderr = process.communicate()
if process.returncode !=0:
    print(stderr)
print(stdout)