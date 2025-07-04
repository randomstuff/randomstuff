#!/usr/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2017 Gabriel Corona
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
splitapparmor - Split ASCII Armor (or PEM) files into multiple files
"""

import re
import sys

RE = re.compile("^-----(BEGIN|END) ([A-Z0-8]*)-----$")

def split_file(filename):
    i = 0
    lines = []
    kind = None
    with open(filename, "rt") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            match = RE.match(line)
            if len(lines) == 0:
                if match and match.group(1) == "BEGIN":
                    kind = match.group(2)
                    lines.append(line)
            elif match and match.group(1) == "END" and kind == match.group(2):
                lines.append(line)
                with open(filename + "." + str(i), "wt") as out:
                    out.write("".join(lines))
                lines.clear()
                kind = None
                i = i + 1
            else:
                lines.append(line)
        if len(lines) != 0:
            raise Exception("File not terminated properly")

filenames = sys.argv[1:]
for filename in filenames:
    split_file(filename)
