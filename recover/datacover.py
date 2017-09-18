#!/usr/bin/python

import subprocess as sub
import os
import re
import multiprocessing as mu
user='dbuser'
pwd='123456'
path='/root/python/test/bak'
alist=[]
dict={}


class Mainfunc():
     def __init__(self,cmd):
        self.cmd = cmd
     
     def subcommand(self):
        try:
           ret = sub.Popen(self.cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
           out,err = ret.stdout.read(),ret.stderr.read()
           if err:
              print("Something wrong ,reason is %s" % err.decode('gb2312').strip())

        except Exception as f :
           print("Some errors,reason is %s" % f )



cmd = "gunzip %s/*.sql.gz" % path
gun = Mainfunc(cmd)
gun.subcommand()
sourcelist=os.listdir(path)


def get_name():
    for n in sourcelist:
        name,a,b = n.split('.')
        cmd = "cat list.txt| grep %s | awk '{print $8}'" % name
        child = sub.Popen(cmd,shell=True,stdout=sub.PIPE)
        res = child.stdout.read().decode('gb2312').strip()
        if res == '':
           print("Cannot find %s in list.txt..." % name)
 
        global dict
        dict[name]=(res,n)

def sqlcommand(gamedb,db,source):
    sqlconnect = "mysql -u%s -h%s -p%s" % (user,db,pwd)
    sqlcmd = [sqlconnect + " -e 'drop  database if exists %s ;'" % gamedb,\
              sqlconnect + "  < %s/%s " % (path,source)]

    print("%s is start... %s " % (gamedb,os.getpid()))
    for s in sqlcmd:
        print(s)
        conn = Mainfunc(s)
        conn.subcommand()
    print("%s is done... %s" % (gamedb,os.getpid()))
    print()


if __name__=="__main__":
    get_name()
    p = mu.Pool(processes=5)
    for k,v in dict.items():
       p.apply_async(sqlcommand,(k,v[0],v[1]))
    p.close()
    p.join()

   

