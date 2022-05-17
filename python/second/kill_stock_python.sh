#!/bin/bash
Date=`date "+%Y%m%d"`
Share='sz300059'
mysql -u root -p123456 share_index -e "delete from ${Share} where DATE = '${Date}' and TIME like '13:00%' order by DIFFERENCE DESC limit 1;"
root@RJKJ-HKT-Kafka-Prod:/opt/share_project/sz300059/second# cat kill-share-python.sh 
#!/bin/bash
Index='sz300059/second'
CMDI=`ps -aux |grep ${Index}  |grep -v color |grep -v dog |awk '{print $2}'`
kill -9 $CMDI
