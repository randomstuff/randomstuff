#!/usr/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2024 Gabriel Corona
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
Summary
-------

Receive sockets using the LISTEN_FDS, accept connections and pass them to a inetd style daemon.
"""

import os
import socket
import selectors
import signal
import sys

selector = selectors.DefaultSelector()


def reap(sig, frame):
    os.wait()


def accept(sock, mask):
    conn, addr = sock.accept()
    pid = os.fork()
    if pid == 0:
        try:
            sock.close()
            os.dup2(conn.fileno(), 0)
            os.dup2(conn.fileno(), 1)
            conn.close()
            os.execvp(sys.argv[1], sys.argv[1:])
        finally:
            os._exit(255)
    else:
        conn.close()


signal.signal(signal.SIGCHLD, reap)

listen_fds = int(os.environ["LISTEN_FDS"])
del os.environ["LISTEN_FDS"]

listen_pid = int(os.environ["LISTEN_PID"])
if listen_pid != os.getpid():
    raise Exception("Unexpected PID")
del os.environ["LISTEN_PID"]

if "LISTEN_FDNAMES" in os.environ:
    del os.environ["LISTEN_FDNAMES"]


for i in range(listen_fds):
    fd = 3 + i
    sock = socket.socket(fileno=fd)
    sock.set_inheritable(False)
    selector.register(sock, selectors.EVENT_READ, accept)

while True:
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
