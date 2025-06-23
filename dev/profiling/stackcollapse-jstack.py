#!/usr/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2022 Gabriel Corona
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Alternative to https://github.com/brendangregg/FlameGraph/blob/master/stackcollapse-jstack.pl
#
# Differences:
# ============
#
# * Includes samples where the thread is in a waiting state.
# * Option to mark samples where the thread is in waiting state.

import sys
import re
from dataclasses import dataclass
import argparse
from typing import List, Optional


# eg. "main" #1 prio=5 os_prio=0 cpu=15,63ms elapsed=0,90s tid=0x00007f0f1c016dc0 nid=0x9dcd waiting on condition  [0x00007f0f22727000]
THREAD_LINE = re.compile('^"([^"]+)" #([0-9]+) ')

# eg. "pool-12-thread-1" prio=5 Id=86 TIMED_WAITING
THREAD_LINE2 = re.compile('^"([^"]+)" prio=[0-9]+ Id=([0-9]+) ')

# eg.   java.lang.Thread.State: TIMED_WAITING (sleeping)
THREAD_STATE_LINE = re.compile(r"^\s+java\.lang\.Thread\.State: ([A-Z_]+)")

# eg.  at java.lang.Thread.sleep(java.base@17.0.2/Native Method)
AT_LINE = re.compile(r"^\s+at ([^\(]+)\(([^\)]+)")

INFO = re.compile(":([0-9]+)$")


@dataclass
class Sample:
    tname: str
    tid: int
    stack: List[str]
    # See https://docs.oracle.com/en/java/javase/12/docs/api/java.base/java/lang/Thread.State.html
    state: str = ""


WAITING_STATES = ["WAITING", "TIMED_WAITING", "LOCKED"]


def main():

    parser = argparse.ArgumentParser(
        description="Generate flamegraph stacks from jstack/jcmd output",
        allow_abbrev=False,
    )
    parser.add_argument(
        "infiles", nargs="*", type=argparse.FileType("rt"), default=[sys.stdin]
    )
    parser.add_argument(
        "--line-numbers", default=True, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--short-line-numbers", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--state",
        dest="show_state",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--streaming", default=True, action=argparse.BooleanOptionalAction
    )

    args = parser.parse_args()
    line_numbers: bool = args.line_numbers
    show_state: bool = args.show_state
    short_line_numbers: bool = args.short_line_numbers
    streaming: bool = args.streaming

    stacks = {}

    def commit(sample: Sample):
        if not sample.stack:
            return
        if sample.state == "NEW" or sample.state == "TERMINATED":
            return

        thread = sample.tname + "#" + str(sample.tid)

        suffix = ""
        if show_state and sample.state:
            suffix = ";" + sample.state
        stack = thread + ";" + ";".join(sample.stack) + suffix
        if streaming:
            print(stack + " 1")
        else:
            stacks[stack] = stacks.get(stack, 0) + 1

    sample: Optional[Sample] = None

    print(args.infiles)
    for infile in args.infiles:
        for line in infile:
            line = line.rstrip()

            if not line:
                if sample is not None:
                    commit(sample)
                    sample = None
                continue

            match = THREAD_LINE.match(line)
            if match is None:
                match = THREAD_LINE2.match(line)
            if match is not None:
                sample = Sample(
                    tname=match.group(1),
                    tid=int(match.group(2)),
                    stack=[],
                )
                continue
            if sample is None:
                continue

            match = THREAD_STATE_LINE.match(line)
            if match is not None:
                sample.state = match.group(1)
                continue

            match = AT_LINE.match(line)
            if match is not None:
                code = match.group(1)
                info = match.group(2)

                match2 = INFO.search(info)
                if match2 is not None and line_numbers:
                    line = match2.group(1)
                    if short_line_numbers:
                        sample.stack.insert(0, ":" + str(line))
                    else:
                        sample.stack.insert(0, code + ":" + str(line))
                sample.stack.insert(0, code)

        if sample is not None:
            commit(sample)
            sample = None

    if not streaming:
        for stack, count in stacks.items():
            print(stack + " " + str(count))


if __name__ == "__main__":
    main()
