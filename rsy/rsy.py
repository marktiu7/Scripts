#!/usr/bin/python

import os
import pexpect
import file
import threading

passwd='123456'
iplist=[]
dirlist=[]
errorlist=[]
def ry_con(ip,passwd,dir):

  ry = pexpect.spawn("rsync -aP --delete /home/test/ root@%s:/home/%s/" %(ip,dir))

  try:
    i=ry.expect(["password:","continue connecting (yes/or)?"],timeout=5)
    if i == 0:
       ry.sendline(passwd)
    elif i==1:
       ry.sendline("yes\n")
       ry.expect("password:")
       ry.sendline(passwd)

    print  '\033[1;31;40m'
    print ("%s is started...." %(ip))
    r = ry.read()
    print r
    print '\033[0m'

  except Exception ,ex:
      print  '\033[1;31;40m'
      print ("ip  %s is failed..." %(ip))
      errorlist.append(ip)
      print '\033[0m'


if __name__=='__main__':
 
 userinput = raw_input("Do you really want to run this script[y/n]:")
 if userinput is not 'y':
    print("sorry")
 else:
    file.open_file(iplist,0)
    file.open_file(dirlist,1)

    def run_zip():
       for ip,dir in zip(iplist,dirlist):
          ry_con(ip,passwd,dir)

    a=threading.Thread(target=run_zip,args=())
    a.start()  

  
    print errorlist
