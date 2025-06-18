#!/usr/bin/python3

from typing import List, Optional
import click
import re
import datetime
import time
import subprocess

ZERO = datetime.timedelta(0)


class DurationType(click.ParamType):
    name = "duration"

    def convert(self, value, param, ctx):
        if isinstance(value, datetime.timedelta):
            return value

        if isinstance(value, (int, float)):
            return datetime.timedelta(seconds=value)

        try:
            if re.fullmatch("[0-9]+", value):
                return datetime.timedelta(seconds=int(value))
            if re.fullmatch("[0-9]+\\.[0-9]+", value):
                return datetime.timedelta(seconds=float(value))
            # TODO, 5s, etc.
            # TODO, ISO duration
            # TODO, 5Hz
        except ValueError:
            pass

        self.fail(f"{value!r} is not a valid duration")


DURATION = DurationType()


# TODO, add support for sqlparse.parsestream?
@click.command
@click.option("--errexit/--no-errexit", "-e", default=False)
@click.option("--interval", "-n", type=DURATION, default="1")
@click.option("--count", "-c", type=int, required=False)
@click.argument("args", nargs=-1)
def main(errexit=False, interval=datetime.timedelta(1), args=[], count=None):
    """
    Execute a given command at regulat interval.

    It is like watch but does not mess with stdio.

    This can be used for collecting metric, profiling, etc.

    Examples:

        megalopoll -n 0.01 gdb -ex "set pagination 0" -ex "thread apply all bt" -batch -p "$pid" > app.gdbstacks

        megalopoll -n 0.01 stack -p "$pid" > app.stacks

        megalopoll -n 0.01 jstack -l "$pid" > app.jstacks

        megalopoll -n 0.01 jcmd Thread.print "$pid" > app.jstacks

        megalopoll -n 0.01 mysql -e"SELECT info FROM INFORMATION_SCHEMA.PROCESSLIST where info is not NULL and db != 'information_schema';" -B -h 127.0.0.1 -u foo -pxoxo > app.sql
    """
    interval_s = interval.total_seconds()
    if count is not None:
        for _ in range(count):
            res = subprocess.run(args)
            if errexit and res.returncode != 0:
                exit(res.returncode)
            time.sleep(interval_s)
    else:
        while True:
            res = subprocess.run(args)
            if errexit and res.returncode != 0:
                exit(res.returncode)
            time.sleep(interval_s)


if __name__ == "__main__":
    main()
