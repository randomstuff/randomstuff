# Some profiling tools

* pmp, Poor man's profiler
* stackcollapse-jstack, process stack samples from jstack/cmd
* symbolicate-elfutils, symbolicate elfutils stack samples using /tmp/perf-$pid.map
* aggregate-counts, aggregate (count or sum) input lines
* megalopoll, polling command, simple building block for Poor man's profiling

For SQL:

* pmp-mysql, Poor man's profiler for MySQL/MariaDB requests
* normalize-sql, normalize SQL

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
