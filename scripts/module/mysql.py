#!/usr/bin/python


import sys
import subprocess as sub
from port11306 import diff_port
user="#######"
pwd="######"
def conn():
  try:
     ip=sys.argv[1]
     if ip in diff_port():
        port=11306
     else:
        port=3306
     cmd="mysql -u{} -P{}  -h{} -p{}".format(user,port,ip,pwd)
     print(cmd)
     sub.call(cmd,shell=True)
  except IndexError:
     print("You must input mysqlip...")
  except Exception as ex:
     print(ex)


conn()
