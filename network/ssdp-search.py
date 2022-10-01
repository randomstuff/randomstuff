#!/usr/bin/python3

"""
Launch a SSDP search request and dump responses
"""

import socket
from signal import alarm
import sys

# TODO, use click
interface_address = sys.argv[1] if len(sys.argv) >= 2 else "0.0.0.0"
service_type = sys.argv[2] if len(sys.argv) >= 3 else "ssdp:all"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.setsockopt(
    socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface_address)
)

message = (
    b"""M-SEARCH * HTTP/1.1\r
HOST: 239.255.255.250:1900\r
MAN: "ssdp:discover"\r
MX: 5\r
ST: """
    + service_type.encode("ASCII")
    + b"""\r
USER-AGENT: Python/3.0 UPnP/1.1 Foo/1.0\r
\r
"""
)

sock.sendto(message, ("239.255.255.250", 1900))
alarm(15)
while True:
    response = sock.recv(4096)
    sys.stdout.write(response.decode("UTF-8"))
    sys.stdout.flush()
