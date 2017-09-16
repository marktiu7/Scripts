#!/usr/bin/python

import time,sys,threading,os
import subprocess as sub

user='dbuser'
pwd='123456'
path="/root/python/test/bak"
t=1
dbnamelist=[]
dblist=[]


class Mainfunc():
     def __init__(self,cmd):
       self.cmd=cmd
     
     def subcommand(self):
       try:
         ret = sub.Popen(self.cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
         out,err = ret.stdout.read(),ret.stderr.read()
         if err:
            print("Something wrong...,the reason is %s" % err.decode('gb2312'))
       except Exception as f:
         print(f)


cmd = "gunzip %s/*.sql.gz " % path
un = Mainfunc(cmd)
#print("All of things will be unziped...")
un.subcommand()
#print("Fininshed!!!")
sourcelist=os.listdir(path)
    
def get_dbname():
    for i in sourcelist:
        dbname,*m = i.split('.')
        dbnamelist.append(dbname)
        print(dbnamelist)

    for db in dbnamelist:
        cmd = "cat list.txt| grep %s | awk '{print $8 }'" % db
        child = sub.Popen(cmd,shell=True,stdout=sub.PIPE)
        res = child.stdout.read().decode('gb2312')
        if res == '':
           print("Cannot find %s in list.txt..."% db)
        else:
           dblist.append(res.replace('\n',''))

def sqlcommand():
  try:
    for dbname,db,source in zip(dbnamelist,dblist,sourcelist):
        sqlconnect = "mysql -u%s -h%s -p%s" % (user,db,pwd)
        sqlcmd = [ sqlconnect + " -e 'drop  databases %s if exists;'" % dbname,
                  sqlconnect + "  < %s/%s " % (path,source)]
                     
    for s in sqlcmd:
        recov = Mainfunc(s)
        recov.subcommand()

    global t
    t = 0.01    
  except Exception as f:
    print(f)

  
def view_bar():
 try:
   for i in range(0,101):
      time.sleep(t)
      rate = i /100
      rate_num= int(rate*100)
      r = '\r[%s%s]%d%%' %("="*i," "*(100-i),rate_num)
      sys.stdout.write(r)
      sys.stdout.flush()
   print()
 except Exception as f :
      print(f)
 

def mupt():
    thlist=[]
    s = threading.Thread(target=sqlcommand)
    v = threading.Thread(target=view_bar)
    s.start()
    v.setDaemon(True)
    v.start()
    s.join()

if __name__=="__main__":
   get_dbname()
   mupt()
