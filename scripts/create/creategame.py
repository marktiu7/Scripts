#!/usr/bin/python

import sys
sys.path.append("/")
from data.lyadmin.scripts.module import command,pathkey
import subprocess as sub
import socket
import configparser
file= "/data/lyadmin/scripts/create/gamecreate.txt"
path="/data/lyadmin/source/cfg"
cfgfile=path+"/lord.cfg"
user="#####"
pwd="#####"


def Isopen(ip,port,gamepath,sid,lord,gamedb,db,key):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
       s.connect((ip,int(port)))
       s.shutdown(2)
       print("{}'s {} is still using...".format(ip,port))
    except:
       Isgamedb(ip,port,gamepath,sid,lord,gamedb,db,key)


def Isgamedb(ip,port,gamepath,sid,lord,gamedb,db,key):
    cmd ="mysql -u{} -h{} -p{} -e 'use {};'".format(user,db,pwd,gamedb)
    ret = sub.Popen(cmd,shell=True,stderr=sub.PIPE)
    if ret.stderr.read():
       print("db {} in {} has already  exits!!!".format(gamedb,db))
    else:
      modifycfg(ip,port,gamepath,sid,lord,gamedb,db,key)


def modifycfg(ip,port,gamepath,sid,lord,gamedb,db,key):
    try:
      cf =configparser.configparser()
      cf.read(cfgfile)
      cf.set("lord","Port",port)
      cf.set("Paysys","PID_SID",sid)
      cf.set("DBSecure","HostName",db)
      cf.set("DBSecure","DBName",gamedb)
      cf.write(open(cfgfile, "w"))
      
      rsgame(ip,gamepath,lord,key)
    except Exception as ex:
      print(ex)

def rsgame(ip,gamepath,lord,key):
     cmd = "rsync -ae 'ssh -i {}' --delete --exclude=logs/ {}/  root@{}:/data/game/{}".format(key,path,ip,gamepath)
     command.localcommand(cmd,lord,"rsync")


def main():
 with open(file) as f:
    while True:
       line = next(f,None)
       if line is None:
         break
       ip,port,gamepath,sid,lord,gamedb,db=line.split()
       key=pathkey.pwdkey(ip)
       Isopen(ip,port,gamepath,sid,lord,gamedb,db,key)       
    

