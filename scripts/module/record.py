#!/usr/bin/python


import datetime


now=datetime.datetime.now()
d1=now - datetime.timedelta(hours=1)
t=d1.strftime("%Y-%m-%d %H:%M:%S")


def log(striptname,file):
       def deco(func):
           def wapper(*args):
               res = func(*args)
               if res !=None:
                 alist=[t,' ','{}'.format(striptname),' ',res]
                 with open('/data/lyadmin/scripts/log/{}'.format(file),'a') as f:
                      for i in alist:
                          f.write(i)
               else:
                 pass 
           return wapper
       return deco
