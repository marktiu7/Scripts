#!/usr/bin/python

import subprocess as sub

cmd = "rsync -a --delete /data/lyadmin/scripts /data/lyadmin/cdk  /data/lyadmin/source /data/backfile"

sub.call(cmd,shell=True)
