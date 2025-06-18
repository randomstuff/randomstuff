# Some profiling tools

## SQL

Collect MySQL/MariaDB statistics for 10s and output the top 10 requests:

~~~sh
/usr/bin/timeout 10s pmp-mysql -u mydb -p xoxo |
normalize-sql --parameterize > samples.sql

cat samples.sql |
aggregate-counts --normalize=percent |
head -n 10
~~~

Or in one command:

~~~sh
(/usr/bin/timeout 10s pmp-mysql -u mydb -p xoxo || true) |
normalize-sql --parameterize |
aggregate-counts --normalize=percent |
head -n 10
~~~
