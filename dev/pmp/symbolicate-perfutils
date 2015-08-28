#!/usr/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2014 Gabriel Corona
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


# This filter replace symbols from /tmp/perf-$pid.map files in
# elfutils stack output. The /tmp/perf-$pid.map are loaded
# automatically.
#
# Input:
#
#   PID 2851 - process
#   TID 2851:
#   #0  0x00007f80b0a983b9 pselect
#   #1  0x00000000005d5363
#   #2  0x000000000059a4f6
#   #3  0x00000000004f2091
#   #4  0x00000000004f5942
#   #5  0x00000000004f6a7f
#   #6  0x00000000004f87f0
#   #7  0x000000000055b487
#   #8  0x00000000004eacfe
#   #9  0x000000000055b36b
#   #10 0x00000000004ef317
#   #11 0x00000000004ef630
#   #12 0x00000000004185d9
#   #13 0x00007f80b09dab45 __libc_start_main
#   #14 0x000000000041908e
#   TID 2852:
#   #0  0x00007f80b0a9653d poll
#   #1  0x00007f80b4f35ebc g_main_context_iterate.isra.29
#   #2  0x00007f80b4f35fcc g_main_context_iteration
#   #3  0x00007f80b4f36009 glib_worker_main
#   #4  0x00007f80b4f5c955 g_thread_proxy
#   #5  0x00007f80b0f8c0a4 start_thread
#   #6  0x00007f80b0a9f07d __clone
#   PID 2851 - process
#   TID 2851:
#   [...]
#
# Perf map file (/tmp/perf-2851.map):
#
#
#    5d5363 500 foo
#
# Output:
#
#   PID 2851 - process
#   TID 2851:
#   #0  0x00007f80b0a983b9 pselect
#   #1  0x00000000005d5363 foo
#   #2  0x000000000059a4f6
#   #3  0x00000000004f2091
#   #4  0x00000000004f5942
#   #5  0x00000000004f6a7f
#   #6  0x00000000004f87f0
#   #7  0x000000000055b487
#   #8  0x00000000004eacfe
#   #9  0x000000000055b36b
#   #10 0x00000000004ef317
#   #11 0x00000000004ef630
#   #12 0x00000000004185d9
#   #13 0x00007f80b09dab45 __libc_start_main
#   #14 0x000000000041908e
#   TID 2852:
#   #0  0x00007f80b0a9653d poll
#   #1  0x00007f80b4f35ebc g_main_context_iterate.isra.29
#   #2  0x00007f80b4f35fcc g_main_context_iteration
#   #3  0x00007f80b4f36009 glib_worker_main
#   #4  0x00007f80b4f5c955 g_thread_proxy
#   #5  0x00007f80b0f8c0a4 start_thread
#   #6  0x00007f80b0a9f07d __clone
#   PID 2851 - process
#   TID 2851:
#   [...]


import re
import sys

stdin = sys.stdin
stdout = sys.stdout
stderr = sys.stderr

perf_re   = re.compile("^([0-9a-fA-F]*) ([0-9a-fA-F]*) (.*)$")
pid_re    = re.compile("^PID ([0-9]*)")
entry_re  = re.compile("^#[0-9]* *0x([0-9a-fA-F]*)$")

class Symbol:
    def __init__(self, start, size, name):
        self.start = start
        self.end = start + size
        self.name = name

# Read a /tmp/perf-pid.map file:
def read_map(filename):
    res = []
    with open(filename, "r") as f:
        for line in f:
            match = perf_re.match(line)
            if match:
                start = int(match.group(1), 16)
                size  = int(match.group(2), 16)
                name  = match.group(3)
                res.append(Symbol(start, size, name))
    res.sort(key = lambda x: x.start)
    return res

maps = {}

# Find the map file for the process:
def get_map(pid):
    perf_map = maps.get(pid)
    if perf_map != None:
        return perf_map
    try:
        perf_map = read_map("/tmp/perf-" + str(pid) + ".map")
    except:
        perf_map = {}
    maps[pid] = perf_map
    return perf_map

# Do a binary each in the map file in order to find the symbol:
def lookup(perf_map, address):
    i = 0
    j = len(perf_map)
    if j == 0:
        return None
    while(True):
        if (j < i):
            return None
        k = round((j + i) // 2)
        if (address < perf_map[k].start):
            j = k - 1
        elif (address >= perf_map[k].end):
            i = k + 1
        else:
            return perf_map[k].name

perf_map = {}

# Process stdin:
for line in stdin:
    match = pid_re.match(line)
    if match:
        pid = int(match.group(1))
        perf_map = get_map(pid)
        stdout.write(line)
        continue
    match = entry_re.match(line)
    if match:
        address = int(match.group(1), 16)
        symbol = lookup(perf_map, address)
        if symbol != None:
            stdout.write(line.rstrip('\n') + " " + symbol + "\n")
        else:
            stdout.write(line)
        continue
    stdout.write(line)
