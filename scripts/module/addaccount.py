#!/usr/bin/python


import subprocess as sub
from port11306 import diff_port

dbuser='#######'
dbpwd='########'


def com(ip,game,user,pwd):
  try:
    if ip in diff_port():
       port=11306
    else:
       port=3306
    sql = 'INSERT INTO %s.account(AccountName,PASSWORD,Activated,CreateTime) VALUES("%s","%s",1,now());' % (game,user,pwd)
    cmd = "mysql -u{} -h{} -P{} -p{} -e'{}'".format(dbuser,ip,port,dbpwd,sql)
    ch = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
  #  print(cmd)
    err = ch.stderr.read().decode('utf-8').strip()
    if err:
       print(err)

  except Exception as ex:
    print(ex)


def main():
   with open("account.txt") as f:
      while True:
         line=next(f,None)
         if line is None:
             break
         ip,game,user,pwd=line.split()
         com(ip,game,user,pwd)


if __name__=="__main__":
    main()
  
      
