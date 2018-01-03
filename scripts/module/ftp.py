#!/usr/bin/python

from ftplib import FTP

ftpip="######"
user="####"
pwd="#####"

def upload(path,remotepath,localpath):
 try:
    ftp = FTP()
    ftp.connect(ftpip,21)
    ftp.login(user,pwd)
    bufsize=4096
    ftp.mkd(path)
    fp=open(localpath,'rb')
    ftp.storbinary("STOR " + remotepath,fp,bufsize)
    fp.close()
 except Exception as ex:
    print(ex)

 
upload('today','today/b.zip','cb.zip')   
