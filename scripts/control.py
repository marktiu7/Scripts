#!/usr/bin/python
# -*- coding:utf-8 -*-
#控制停服和起服

import sys
import multiprocessing as mult
from module import pathkey,command
from module import concrontab
import subprocess as sub

file="/data/lyadmin/scripts/list.txt"
err=[]

#判断是否重复启动
def mulplord(ip,key,lord):
       cmd = "ps aux | grep %s | grep -v grep " % lord
       return (command.remotecommand(ip,cmd,key,lord,"start",flag=True))
      

#根据状态选择需要执行的语句
def switchoption(sw,ip,path,lord,key):
    changepath="cd /data/game/%s;" % path

    if sw =="stop":
       cmd = changepath+"killall -10  %s" % lord

    elif sw=="start":
       print(mulplord(ip,key,lord))
       if mulplord(ip,key,lord):
          print("%s is still running..." % lord)
          err.append(lord)
          cmd = False
       else:
          cmd = changepath + "chmod +x lord;cp -arf lord %s ; ./%s -d " % (lord,lord)
    else:
       print("You must input right command[start]/[stop]")
       cmd= False
    return cmd

#主要执行函数
def mainfunc(status):
   p = mult.Pool(processes = 5)
   with open(file) as f:
       line = f.readlines()
       for data in line:
           ip,port,path,lord,gamedb,db=data.split()
           key=pathkey.pwdkey(ip)
           cmd =switchoption(status,ip,path,lord,key)
           p.apply_async(command.remotecommand,(ip,cmd,key,lord,status))
       p.close()
       p.join() 
       print("") 
       print("Everything is done...")     
             
if __name__=="__main__":
  try:
    input=sys.argv[1]
    if input=="stop":
       concrontab.stop("scan.py")

    elif input=="start":
       concrontab.start("scan.py")
    
    mainfunc(input)

#如果有重复启动，会显示出来
    if err:
       print(err)
  except IndexError:
       print("You need to input command [start] or [stop]")
