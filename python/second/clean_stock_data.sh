#!/bin/bash
Date=`date "+%Y%m%d"`
Share='sz300059'
mysql -u root -p123456 share_index -e "delete from ${Share} where DATE = '${Date}' and TIME like '13:00%' order by DIFFERENCE DESC limit 1;"
