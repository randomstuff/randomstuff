#!/usr/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Gabriel Corona
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
Executed on a Ganeti node, this should open a connection to the VNC
endpoint of a requested instance and connect it to stdin/stdout.

Usage:
------

Associate this to an SSH key on the gateway (~vncrelay/authorized_keys):

~~~
ssh-ed25519 AAAA... user@host command="gnt-instance-vnc-connect instance_name" restrict
~~~

It should be able to talk to the Ganeti RAPI in order to find the address of
the VNC endpoint and it should be able to connect to it.

On the client side, setup a tunnel:

~~~sh
socat TCP-LISTEN:9999,bind=127.0.0.1 EXEC:"ssh -T vncrelay@node_name"
~~~
"""

from requests import get
from requests.auth import HTTPBasicAuth
from sys import argv, exit
from os import execlp

# Change me!
url = "https://example.com:5080"
username = "..."
password = "..."

instance = argv[1]

auth = HTTPBasicAuth(username, password)

response = get(url + "/2/instances/" + instance, verify=False, auth=auth)
if response.status_code != 200:
    exit(1)
json = response.json()

address = json["hvparams"]["vnc_bind_address"]
port = json["network_port"]
execlp("socat", "socat", "STDIO", "TCP:%s:%s" % (address, port))
exit(255)
