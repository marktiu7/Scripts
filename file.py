#!/usr/bin/python

import os


def open_file(alist,num):
 path='ip.txt'
 try:
    if os.path.exists(path):
       with open(path) as f:
         data=f.readlines()
         for line in data:
            line=line.replace('\n','').split()
            alist.append(line[num])

    else:
        print ("Sorry.Cannot find the file!!!")


 except Exception.ex:

    print ("Some error")



