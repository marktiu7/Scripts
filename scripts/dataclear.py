#!/usr/bin/python
# -*- coding:utf-8 -*-

from module import command,pathkey,concrontab
import subprocess as sub
import time

#先判断账号数量，备份，停服，删库，重启


user="#######"
pwd="#######"
file= "/data/lyadmin/scripts/clear.txt"
datepath=time.strftime("%Y%m%d%H%M")
dumppath="/data/lyadmin/backup/clearbak"

#判断目标库种的账号数量，大于5则不能清除，小于5继续执行
def juide(ip,key,path,lord,gamedb,db):
  try:
    cmd="mysql -u{} -h{} -p{} -N -e 'select count(*) from {}.account' ".format(user,db,pwd,gamedb)
    ret=sub.Popen(cmd,shell=True,stdout=sub.PIPE)
    out= ret.stdout.read().decode().strip()
    if int(out) > 5 :
       print("There are {} roles in {},so you cannot drop it.".format(out,gamedb))
    else:
       mainfunc(ip,key,path,lord,gamedb,db)

  except Exception as ex:
    print(ex)

#备份目标库
def backup(db,gamedb):
    cmd = "mysqldump -h%s -u%s -p%s -R -B %s | gzip > %s/%s.%s.sql.gz " \
                        % (db,user,pwd,gamedb,dumppath,gamedb,datepath)
    sub.call(cmd,shell=True)

#停服，备份，删库，重启     
def mainfunc(ip,key,path,lord,gamedb,db):
  try:
    
    pathcmd="cd /data/game/{}; ".format(path)
    stopcmd="killall -10 {}".format(lord)
    command.remotecommand(ip,stopcmd,key,lord,status="stop")
    
    backup(db,gamedb)

    mysql="mysql -u{} -h{} -p{}  ".format(user,db,pwd)
    cmd = mysql+"-e 'drop database if exists {};' ".format(gamedb)
    command.localcommand(cmd,lord,"drop")
  
    startcmd=pathcmd+ "./{} -d".format(lord)
    command.remotecommand(ip,startcmd,key,lord,status="create")

  except Exception as ex:
    print(ex)

def run():
    with open(file) as f:
      while True:
         line=next(f,None)
         if line is None:
            break
         ip,port,path,lord,gamedb,db=line.split()
         key=pathkey.pwdkey(ip)
         juide(ip,key,path,lord,gamedb,db)

if __name__=="__main__":
        concrontab.stop("scan.py")
        run()
        concrontab.start("scan.py")
