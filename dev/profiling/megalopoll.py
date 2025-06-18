#!/usr/bin/python3

import argparse
import re
import datetime
import time
import subprocess


def parse_duration(value: str) -> datetime.timedelta:

    m = re.match("^([.0-9]+)([a-zA-z]*)$", value)
    if m:
        value = float(m.groups()[0])
        unit = m.groups()[1]

        # No unit = seconds:
        if unit == "s":
            return datetime.timedelta(seconds=value)

        # SI units:
        if unit == "":
            return datetime.timedelta(seconds=value)
        if unit == "ms":
            return datetime.timedelta(milliseconds=value)
        if unit == "us":
            return datetime.timedelta(microseconds=value)
        if unit == "Hz":
            return datetime.timedelta(seconds=1 / value)
        if unit == "kHz":
            return datetime.timedelta(seconds=1 / (1000 * value))

    # TODO, ISO duration ("PT5S")
    raise ValueError("Invalid duration value")


description = """
Generic polling tool, executes a given command at regulat interval.
It works somewhat like 'watch' but does not mess with your stdio.
This can be used for collecting metric, profiling, etc.
"""

epilog = """
Examples:

    megalopoll -n 0.01 gdb -ex "set pagination 0" -ex "thread apply all bt" -batch -p "$pid" > app.gdbstacks
    megalopoll -n 0.01 stack -p "$pid" > app.stacks
    megalopoll -n 0.01 jstack -l "$pid" > app.jstacks
    megalopoll -n 0.01 jcmd Thread.print "$pid" > app.jstacks
    megalopoll -n 0.01 mysql -e"SELECT info FROM INFORMATION_SCHEMA.PROCESSLIST where info is not NULL and db != 'information_schema';" -B -h 127.0.0.1 -u foo -pxoxo > app.sql
"""


def main():

    parser = argparse.ArgumentParser(
        description=description,
        allow_abbrev=False,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--errexit",
        "-e",
        action=argparse.BooleanOptionalAction,
        help="Stops if the command fails",
    )
    parser.add_argument(
        "--interval",
        "-n",
        required=False,
        help="Polling duration/intervale",
        default="1",
    )
    parser.add_argument(
        "--count", "-c", required=False, type=int, help="Maximum number of executions"
    )
    parser.add_argument(
        "argv",
        nargs=argparse.REMAINDER,
        type=str,
        action="extend",
        help="Program (and arguments) to spawn",
    )
    args = parser.parse_args()

    errexit = args.errexit
    interval = parse_duration(args.interval)
    argv = args.argv
    if argv and argv[0] == "--":
        argv = argv[1:]
    count = args.count

    interval_s = interval.total_seconds()
    if count is not None:
        for _ in range(count):
            res = subprocess.run(argv)
            if errexit and res.returncode != 0:
                exit(res.returncode)
            time.sleep(interval_s)
    else:
        while True:
            res = subprocess.run(argv)
            if errexit and res.returncode != 0:
                exit(res.returncode)
            time.sleep(interval_s)


if __name__ == "__main__":
    main()
