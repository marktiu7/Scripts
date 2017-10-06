#!/usr/bin/python

import os
import socket
import re
import paramiko as pa
import subprocess as sub

user='root'
pwd='JGyou(20170206)$'

def conn(ip,cmd):
  try:
     ssh = pa.SSHClient()
     ssh.load_system_host_keys()
     ssh.set_missing_host_key_policy(pa.AutoAddPolicy)
     ssh.connect(ip,22,user,pwd)
     stdin,stdout,stdder = ssh.exec_command(cmd)
     res,err = stdout.read().decode('utf-8').strip(),stdder.read().decode('utf-8').strip()
     result = res if res else err
     if result =='':
        print('lord starts successful!')
     else:
        print(result)
  except Exception as f :
        print("Something wrong with %s" % f)

def juidelord(ip,lordpath,lord):
     cmdpath = 'cd /data/jzadmin/game/%s; ' % lordpath
     if re.search('[Cc]ros',lord):
        cmd = cmdpath+ './%s server_type=2 lord_file=lord.cfg' % lord
     elif re.search('[Ww]orld',lord):
        cmd = cmdpath+ './%s -d ' % lord
     else:
        cmd = cmdpath + './%s server_type=1 lord_file=lord.cfg ' % lord
     conn(ip,cmd) 


def IsOpen(ip,port,path,lordname):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
       s.connect((ip,int(port)))
       s.shutdown(2)
    except:
       print(" %s is down %s" % (ip,lordname))
       juidelord(ip,path,lordname)

if __name__=='__main__':

   with open("scan.txt") as f:
           line = f.readlines()
           for data in line:
             ip,out,port,path,lord,c,d,e = data.split()
             if len(port) == 4:
               IsOpen(ip,port,path,lord)
             elif len(port) == 12:
               port1 = port[2:6]
               port2 = port[8:]
               if port1 :
                  IsOpen(ip,port1,path,lord)
               elif port2:
                  IsOpen(ip,port2,path,lord)
               else:
                  IsOpen(ip,port1,path,lord)
                  IsOpen(ip,port2,lord)
