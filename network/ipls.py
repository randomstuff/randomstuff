#!/usr/bin/python3

import sys
from ipaddress import ip_network

for arg in sys.argv[1:]:
    for ip in ip_network(arg, strict=False).hosts():
        print(ip)
