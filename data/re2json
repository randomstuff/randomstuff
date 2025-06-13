#!/usr/bin/python3
#
# Parse each line according to some regular expressions and
# generate JSON from named captures.
#
# Example:
#   echo "GET / HTTP/1.1" | ./re2json '^(?P<method>[^ ]*) (?P<path>[^ ]*) (?P<protocol>.*)'$
# Output:
#   {"method": "GET", "path": "/", "protocol": "HTTP/1.1"}

import json
from sys import argv, stdin, stdout
from re import compile


patterns = [compile(arg) for arg in argv[1:]]

for entry in stdin:
    entry = entry.rstrip("\n")
    for pattern in patterns:
        m = pattern.match(entry)
        if m:
            stdout.write(json.dumps(m.groupdict()) + "\n")
            break

