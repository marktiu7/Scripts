# -*- coding: utf-8 -*-
import os
import ftplib
import datetime
 
FTP_SERVER = '####'
FTP_SERVER_PORT = 21
FTP_USER = '####'
FTP_PASSWORD = '####'
 
now = datetime.datetime.now()
tda = now - datetime.timedelta(days=1)
date = tda.strftime("%Y%m%d")
BACKUP_FILE_PATH = '/data/dbbackup/%s/' %(date)

FTP_PATH = '/VOL1/pg-pcs3'
 
#EDIT=============================
#now = datetime.datetime.now()
#tda = now - datetime.timedelta(days=1)
#date = tda.strftime("%Y%m%d")
#BACKUP_FILE_PATH = '/data/dbbackup/%s/' %(date)
#=================================


def ftp_login(ftp, user, password):
	try:
		ftp.login(user, password)
 
	except ftplib.error_perm, err:
		print('login fail : ' + str(err))
		return False
 
	return True
 
 
def ftp_cd(ftp, path):
	patharr = path.split('/')
 
	for a in patharr:
		if a == '': continue
		try:    
			ftp.cwd(a)
		except ftplib.error_perm, err:
			print('cd fail : ' + str(err))
			return False		
 
	if ftp.pwd() == FTP_PATH:
		return True
 
	else:
		return False
 
def ftp_get_filelist(ftp):
#	data = ftp.retrlines('LIST')
#	arr = data.split()
	arr = ftp.nlst()
 
	return arr
 
def ftp_put_file(ftp, filename, filepath):
	print('file send : ' + filename)
 
	fp = open(filepath, 'rb')
	ftp.storbinary('STOR ' + filename, fp)
	fp.close()
 
 
if __name__ == "__main__":
 
	ftp = ftplib.FTP()
 
	ftp.connect(FTP_SERVER, FTP_SERVER_PORT)
 
	if ftp_login(ftp, FTP_USER, FTP_PASSWORD):
		if ftp_cd(ftp, FTP_PATH):
			filelist = os.listdir(BACKUP_FILE_PATH)
			ftpfilelist = ftp_get_filelist(ftp)
 
			for a in filelist:
				if a in ftpfilelist:
					continue
 
				ftp_put_file(ftp, a, BACKUP_FILE_PATH + '/' + a)
 
		else:
			print('Path change fail!')
 
	else:
		print('Login fail!')
	ftp.quit()
