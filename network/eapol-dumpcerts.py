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
Extracts certificates from EAPOL hexdump (eg. when using Wifi PEAP)

Usage:

python3 eapol-dumpcerts.py < frames.hexdump > cert.pem

Expects in stdin the raw bytes lines obtained with:

$ sudo nmcli general logging level TRACE domains WIFI
$ sudo journalctl -S today | grep "RX EAPOL - hexdump" | grep -o '[a-z0-9 ]*$'
"""

import sys
from scapy.layers.eap import EAPOL
from scapy.layers.tls.all import TLS

EAP_METHOD_TYPE_PEAP = 25
TLS_MSGTYPE_CERTIFICATE = 11

raw_packets = [bytes.fromhex(line) for line in sys.stdin if line]
eapol_packets = [EAPOL(raw_packet) for raw_packet in raw_packets]

# Reconstruct EAP frames using "M" flag (more data):
raw_tls_frames = []
current = b""
for p in eapol_packets:
    if p.payload.type == EAP_METHOD_TYPE_PEAP:
        current = current + p.payload.tls_data
        if not p.payload.M and current:
            raw_tls_frames.append(current)
            current = b""
if current:
     raw_tls_frames.append(current)
     current = b""

tls_packets = [TLS(p) for p in raw_tls_frames]
tls_payloads = [q for p in tls_packets for q in p.payload]
tls_msgs = [m for p in tls_payloads for m in p.msg]

for m in tls_msgs:
    # Check type=certificate:
    if m.msgtype == TLS_MSGTYPE_CERTIFICATE:
        for (_, cert) in m.certs:
            print("S:" + cert.subject_str)
            print("I:" + cert.issuer_str)
            print(cert.pem.decode("ASCII"))
