#!/usr/bin/python
# -*- coding:utf-8 -*-
#备份数据库

import time
import subprocess as sub
import os
from module import command
import multiprocessing  as mult

user="#######"
pwd="########"
path="/data/lyadmin/scripts"
dumppath="/data/lyadmin/backup/hefubackup/"
file="list.txt"

#根据日期创建目录
datepath=time.strftime("%Y%m%d%H%M")
if not os.path.exists(dumppath+datepath):
       os.mkdir(dumppath+datepath)

#主要执行函数，使用的是command.localcommand
if __name__=="__main__":
        p=mult.Pool(processes=5)
        with open(file) as f:
             line = f.readlines()
             for data in line:
                 ip,*m,gamedb,db=data.split()
                 cmd = "mysqldump -h%s -u%s -p%s -R -B %s | gzip > %s%s/%s.%s.sql.gz " \
                        % (db,user,pwd,gamedb,dumppath,datepath,gamedb,datepath)
                 p.apply_async(command.localcommand,(cmd,gamedb,"backuped"))
             p.close()
             p.join()
             print("Everything is done...")
