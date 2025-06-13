#!/usr/bin/python3
import msgpack
import json
from sys import stdin, stdout

data = json.load(stdin)
stdout.buffer.write(msgpack.packb(data))
