#!/bin/bash
mysql_dir=`which mysql`
dump_dir="/data/lyadmin/backup/databack"
db_date=`date '+%Y-%m-%d-%H%M%S'`
user="jianzong"
passwd="letmego"
array=(
192.168.0.18
192.168.0.9
192.168.0.10
192.168.0.20
)
mysql_cmd="mysql -u$user  -p$passwd"
dump_cmd="mysqldump -u$user  -p$passwd -R --skip-lock-tables"

##ftp
ftp_user="mysqlbackup"
ftp_passwd="jg_sosogood"
ftp_host="192.168.0.17"
ftp_base_dir="mysqlbackup"
ftp_mk_date=`date '+%Y-%m-%d'`
if [ ! -n $dump_dir ];then
    echo "$dump_dir is empty!"
    exit
else
   find $dump_dir/*.gz -mtime +30 |xargs rm -rf {}\;
fi

ftp_mkdir(){
ftp -i -n<<EOF
open $ftp_host
user $ftp_user $ftp_passwd 
cd mysqlbackup
mkdir LYCQ_game_${ftp_mk_date}
bye
EOF
}
ftp_mkdir



for db_url in ${array[*]}
do
db_list=`$mysql_cmd -h${db_url} -e  "show databases;"|egrep -v "mysql|test|information_schema|performance_schema|*.rewardcode"|sed 1d`
for db_name in $db_list
do
    [ ! -d $dump_dir ] && mkdir  $dump_dir -p
    $dump_cmd -h${db_url} -B $db_name|gzip > $dump_dir/${db_name}_${db_date}.sql.gz
    sleep 1
ftp -i -n<<EOF
open $ftp_host
user $ftp_user $ftp_passwd 
binary
cd mysqlbackup
cd LYCQ_game_${ftp_mk_date}
lcd $dump_dir 
put ${db_name}_${db_date}.sql.gz
quit 
EOF
done
sleep 1
done

