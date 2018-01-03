#!/usr/bin/python

import os
import socket
import paramiko 
import sys,datetime
import logging
sys.path.append('/')
from data.lyadmin.scripts.module import pathkey,record
file="/data/lyadmin/scripts/mainlist.txt"
user="root"
keydict={}


def Portstatus(ip,port,path,lord,key):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
      s.connect((ip,int(port)))
      s.shutdown(2)
    except:
      command(ip,path,lord,key)
#free -m | grep Mem | awk {'print $4'}

@record.log('scan.py','restart.log')
def command(ip,path,lord,key):
  try:
     cmd="cd /data/game/%s; ./%s -d " % (path,lord)
     ssh=paramiko.SSHClient()
     ssh.load_system_host_keys()
     privatekey = os.path.expanduser(key)
     key = paramiko.RSAKey.from_private_key_file(privatekey)
     ssh.connect(ip,22,user,pkey = key)
     stdin,stdout,stderr=ssh.exec_command(cmd)
     out=stdout.read().decode('utf-8').strip()
     err = stderr.read().decode('utf-8').strip()
     rest = out if out else err
     if rest=="":
        return ("{} is restarting...\n".format(lord))
     else:
        return ip,lord,rest
     ssh.close()
  except Exception as ex:
     print(ex)

 

if __name__=="__main__":
     with open(file) as f:
         while True:
              line = next(f,None)
              if line is None:
                    break
              ip,port,path,lord,gamedb,m = line.split()
              key=pathkey.pwdkey(ip)
              Portstatus(ip,port,path,lord,key)
