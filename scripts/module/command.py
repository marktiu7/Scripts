#!/usr/bin/python

import os
import subprocess as sub
import paramiko
import logging
user="root"

def log(func):
      def warpper(*args):
          res=func(*args)
          logging.basicConfig(level=logging.DEBUG,
                              format="%(asctime)%s %(levelname)s %(message)s",
                              datefmt="%a,%d %b %Y %H:%M:%S",
                              filename="myapp.log",
                              filemode="a")
          logging.warning(res)
      return warpper


def shortcmd(cmd):
    try:
        sub.call(cmd,shell=True)
    except Exception as ex:
        print(ex)

def localcommand(cmd,name,status):
    try:
      command = sub.Popen(cmd,shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
      out = command.stdout.read().decode('utf-8').strip()
      err = command.stderr.read().decode('utf-8').strip()
      if err:
         print(" \033[1;31;43m {} \033[0m {} has failed!!!".format(name,status))
      else:
         print("\033[32;1m {} \033[0m has {} successfully!".format(name,status))
    except Exception as ex:
          print(ex)


def remotecommand(ip,cmd,key,name,status,flag=False):
 if cmd !=False:
    try:
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        privatekey = os.path.expanduser(key)
        key = paramiko.RSAKey.from_private_key_file(privatekey)
        ssh.connect(ip,22,user,pkey = key)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8').strip()
        err= stderr.read().decode('utf-8').strip()
        if flag:
           return (out)
        else:
            ret = out if out else err
            if ret !="":
               print("\033[1;31;43m %s \033[0m  wrong,%s" %(name,ret))
               print("")
            else:
               print("\033[32;1m {} \033[0m has {}ed successfully!".format(name,status))
               print("")
        ssh.close()  
    except Exception as ex:
         print(ex)
    
