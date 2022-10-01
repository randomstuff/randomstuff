#!/usr/bin/python3

"""
Listen for SSDP announces and dump responses
"""

import socket
from signal import alarm
import sys
import ipaddress
import struct
import sys

interface_address = sys.argv[1] if len(sys.argv) >= 2 else "0.0.0.0"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
# Not available in Python: sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_ALL, 0)
sock.bind(("0.0.0.0", 1900))

mreq = struct.pack(
    "4s4s", socket.inet_aton("239.255.255.250"), socket.inet_aton(interface_address)
)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    response = sock.recv(4096)
    sys.stdout.write(response.decode("UTF-8"))
    sys.stdout.flush()
