#!/usr/bin/python

pwdfile="/data/lyadmin/cdk/key.txt"
keydict={}


def pwdkey(ip):
   try:
     with open(pwdfile) as f:
          lines = f.readlines()
          for data in lines:
              keyip,path = data.split()
              keydict[keyip]=path
          return keydict[ip]
   except Exception as f:
          print(f) 


