#!/usr/bin/python3

# Execute a program from a pipe, etc. without writing the file to any filesystem.
#
# Usage:
#  python memexec.py -               argv0 args
#  python memexec.py 0               argv0 args
#  python memexec.py /prof/self/fd/0 argv0 args
# Examples:
#  cat /usr/bin/busybox | python3 memexec.py - ls
#  cat /usr/bin/busybox | python3 -c "$(cat memexec.py)" - ls
#  podman run -it --rm --name example docker.io/library/python -c "$(cat memexec.py)" - nc 127.0.0.1 80
#  cat /usr/bin/busybox | podman exec -i example python3 -c "$(cat memexec.py)" - nc 127.0.0.1 80
# Works best with static binaries.

import os
import sys

arg = sys.argv[1]

if arg == "-":
    input_file = sys.stdin.buffer
elif arg.isnumeric():
    input_file = open(int(arg), "rb")
else:
    input_file = open(arg, "rb")

chunk_size = 1024 * 1024
fd = os.memfd_create("")
while True:
    chunk = input_file.read(chunk_size)
    if not chunk:
        break
    n = len(chunk)
    i = 0
    while i < n:
        i += os.write(fd, chunk[i:])
input_file.close()

path = "/proc/self/fd/" + str(fd)
os.execv(path, sys.argv[2:])
