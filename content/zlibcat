#!/usr/bin/python3

"""Uncompress raw zlib data."""

from sys import argv, stdout
from zlib import decompress

for filename in argv[1:]:
    with open(filename, "rb") as f:
        data = decompress(f.read())
    stdout.buffer.write(data)
