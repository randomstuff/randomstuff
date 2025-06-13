#!/bin/sh
# Poor man's profilter. MySQL/MariaDB edition.
# Usage: pmp-mysql -h 127.0.0.1 -u user -pxoxo

sql="SELECT info FROM INFORMATION_SCHEMA.PROCESSLIST where info is not NULL and db != 'information_schema';"

while True; do
    mysql -e"$sql" -B "$@"
    sleep 0.01
done
