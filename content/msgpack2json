#!/usr/bin/python3
import msgpack
import json
from sys import stdin, stdout

data = msgpack.load(stdin.buffer)
stdout.write(json.dumps(data))
