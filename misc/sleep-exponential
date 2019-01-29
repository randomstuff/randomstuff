#!/usr/bin/python3

from sys import argv, stdout, stderr
from time import sleep
from random import expovariate

if len(argv) != 2:
    stderr.write("sleep-exponentiel: bad usage.\n")
    exit(1)

if argv[1] == "--help" or argv[1] == "-v":
    stdout.write("Usage: sleep-exponential PERIOD\n\n")
    stdout.write("  Like 'sleep' but the duration is exponentially distributed.\n")
    stdout.write("  PERIOD is the period (in seconds) i.e. the inverse of the rate (lambda).\n")
    exit(0)

period = float(argv[1])
rate = 1 / period
duration = expovariate(rate)
sleep(duration)
