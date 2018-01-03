#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from   ftplib import FTP
import datetime
 
FTP_SERVER = '####'
FTP_SERVER_PORT = 21
FTP_USER = '####'
FTP_PASSWORD = '######'
 
now = datetime.datetime.now()
tda = now - datetime.timedelta(days=1)
date = tda.strftime("%Y%m%d")
BACKUP_FILE_PATH = '/data/dbbackup/%s/' % (date)

FTP_PATH = '/VOL1/pg-pcs3'
 
#EDIT=============================
#=================================


def ftp_login(host,user,pwd):
    try:
       ftp = FTP()
       ftp.connect(host,21)
       ftp.login(user,pwd)
       ftp.cwd(FTP_PATH)
       if date not in ftp.nlst():
          ftp.mkd(date)
       ftp.cwd(date)
       return ftp
    except Exception, ex:
       print(ex)


def uploadfile(ftp,remotepath,localpath):
    try:
       bufsize=4096
       fp = open(localpath,'rb')
       ftp.storbinary("STOR " + remotepath,fp,bufsize)
       fp.close()
    except Exception,ex:
       print(ex)



if __name__=="__main__":
    ftp=ftp_login(FTP_SERVER,FTP_USER,FTP_PASSWORD)
    for i in os.listdir(BACKUP_FILE_PATH):
        uploadfile(ftp,i,BACKUP_FILE_PATH+i)


