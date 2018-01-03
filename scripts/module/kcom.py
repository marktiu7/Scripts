#!/usr/bin/python

import sys,os
import paramiko 
import pathkey


user="root"
file="/data/lyadmin/scripts/mainlist.txt"

def command(ip,key,cmd,path,flag=False):
    try:
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        privatekey = os.path.expanduser(key)
        key = paramiko.RSAKey.from_private_key_file(privatekey)
        ssh.connect(ip,22,user,pkey = key)
        if flag:
           cmd = "cd /data/game/{}; ".format(path)+cmd
        else:
           cmd = cmd
        stdin,stdout,stderr=ssh.exec_command(cmd)
        out,err = stdout.read().decode().strip(),stderr.read().decode().strip()
        result = out if out else err
        if flag:
           print("{}: ".format(path)+result)
        else:
           print("{}: ".format(ip)+result)
        print("")

    except Exception as ex:
        print(ex)


if __name__=="__main__":

     cmd=input("Please input the command:")
     flag = False
     try:
       if sys.argv[1]:
          flag=True
     except IndexError:
            pass 
    
     with open(file) as f:
          line = f.readlines()
          for data in line:
              ip,port,path,*c=data.split()
              key=pathkey.pwdkey(ip)
              command(ip,key,cmd,path,flag)
