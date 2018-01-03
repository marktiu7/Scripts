#!/usr/bin/python

from ftplib import FTP
import subprocess as sub
import time,os,sys
import multiprocessing  as mult
import logging
sys.path.append("/")
from data.lyadmin.scripts.module import record

ftpip="#######"
user="######"
pwd="######"
uploadpath="/data/lyadmin/backup/databack/"
dbuser="######"
dbpwd="######"

dblist=['#########']

dbdict={}

datepath=time.strftime("%Y%m%d%H%M")
if not os.path.exists(uploadpath+datepath):
       os.mkdir(uploadpath+datepath)


@record.log('myftp.py','myftp.log')
def command(cmd):
  try:
     co = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
     err=co.stderr.read().decode().strip()
     if err!="":
        return err
  except Exception as ex:
     return (ex)

@record.log('myftp.py','myftp.log')
def get_dbname():
   try: 
        for db in dblist:
            cmd = "mysql -h{} -u{} -p{} -N -e 'show databases;'| egrep -v 'mysql|test|information_schema|performance_schema'".format(db,dbuser,dbpwd)
            s=sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
            out =s.stdout.read().decode().strip()
            err =s.stderr.read().decode().strip()
            if err:
              return ("{} haha".format(err))
            else:
              dbdict[db]=out.split()
   except Exception as ex:
        return (ex)


def backuptask(ip,edb):
  try:
    cmd = "mysqldump -h{} -u{} -p{} -R -B {} | gzip > {}{}/{}.{}.sql.gz ".format(ip,dbuser,dbpwd,edb,uploadpath,datepath
     ,edb,datepath)
    command(cmd)
    upload(datepath,"{}.{}.sql.gz".format(edb,datepath),uploadpath+datepath+"/{}.{}.sql.gz".format(edb,datepath))   
  except Excpetion as ex:
    print(ex)



@record.log('myftp.py','myftp.log')
def upload(path,remotepath,localpath):
 try:
    ftp = FTP()
    ftp.connect(ftpip,21)
    ftp.login(user,pwd)
    bufsize=4096
    ftp.cwd("mysqlbackup")
    if path not in ftp.nlst():
         ftp.mkd(path)
    ftp.cwd(path)
    fp=open(localpath,'rb')
    ftp.storbinary("STOR " + remotepath,fp,bufsize)
    fp.close()
 except Exception as ex:
    return(ex)

def mainfunc():
 try:
    p=mult.Pool(processes=5)
    for ip ,mdb in dbdict.items():
        for edb in mdb:
          p.apply_async(backuptask,(ip,edb))
    p.close()
    p.join()
 except Exception as ex:
    print(ex)


if __name__=="__main__":
   get_dbname()
   mainfunc()


