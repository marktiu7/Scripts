#!/usr/bin/python
# -*- coding:utf-8 -*-

#同步游戏服务器资源
from module import command,pathkey
import subprocess as sub
import multiprocessing as mult
file= "/data/lyadmin/scripts/list.txt"
updatepath="/data/lyadmin/source"


def rsync(myinput):
  try:
    with open(file) as f:
         line = f.readlines()
         for data in line:
            ip,port,path,lord,*c=data.split()
            key=pathkey.pwdkey(ip)
            cmd1="rsync -ae 'ssh -i {}'  {}/{}  root@{}:/data/gamebao/".format(key,updatepath,myinput,ip)
            command.localcommand(cmd1,path,"rsync zip")
            cmd2="unzip -o /data/gamebao/{} -d /data/game/{}/ > /dev/null".format(myinput,path) 
            command.remotecommand(ip,cmd2,key,path,"updat")
  except Exception as ex:
         print(ex)          


    
#同步函数
if __name__=="__main__":
    myinput=input("Please input the zip file:")
    rsync(myinput)
