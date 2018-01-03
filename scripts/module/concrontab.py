#!/usr/bin/python


import subprocess as sub


def subcom(name):
    cmd = "crontab -l | grep {}".format(name)
    ret = sub.Popen(cmd,shell=True,stdout=sub.PIPE)
    out = ret.stdout.read().decode('utf-8').strip()
    return out.startswith("*")

def stop(name):
 try:
   if subcom(name):
     cmd="sed -i '/{}/ s/^/#/ ' /var/spool/cron/root".format(name)
     sub.call(cmd,shell=True)
   else:
     pass
 except Exception as ex:
     print(ex)

def start(name):
 try:
   if subcom(name):
     pass
   else: 
     cmd="sed -i '/{}/ s/^#// ' /var/spool/cron/root".format(name)
     sub.call(cmd,shell=True)
 except Exception as ex:
     print(ex)

