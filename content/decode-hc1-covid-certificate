import sys

# https://gitlab.inria.fr/tousanticovid-verif/tousanticovid-verif-android

digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
digit2num = {digit: i for i, digit in enumerate(digits)}
assert len(digits) == 45

# Base 45 decoding: https://datatracker.ietf.org/doc/draft-faltstrom-base45/
def decode_base45(data: str) -> bytes:

    ochunks = []
    for i in range(0, len(data), 3):
        chunk = data[i : i + 3]
        if len(chunk) == 2:
            c = digit2num[chunk[0]]
            d = digit2num[chunk[1]]
            n = c + d * 45
            ochunk = bytes([n])
        elif len(chunk) == 3:
            c = digit2num[chunk[0]]
            d = digit2num[chunk[1]]
            e = digit2num[chunk[2]]
            n = c + d * 45 + e * 45 * 45
            ochunk = bytes([n // 256, n % 256])
        else:
            raise Exception("invalid length")
        ochunks.append(ochunk)

    res = b"".join(ochunks)
    return res


assert decode_base45("BB8") == b"AB"
assert decode_base45("%69 VD92EX0") == b"Hello!!"
assert decode_base45("UJCLQE7W581") == b"base-45"
assert decode_base45("QED8WEX0") == b"ietf!"

data = sys.argv[1]
print(data)

expected_prefix = "HC1:"
if not data.startswith(expected_prefix):
    raise Exception("Invalid prefix")
data = data[len(expected_prefix) :]

decoded = decode_base45(data)
print("Decoded=")
print(decoded)
print("")

import zlib

decompressed = zlib.decompress(decoded)
print("Decompressed=")
print(decompressed)
print("")

import cbor

cose = cbor.loads(decompressed)
print("COSE=")
print(cose)
print("")

# See https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml
# Tag 18 = COSE_Sign1 (COSE Single Signer Data Object) [RFC-ietf-cose-rfc8152bis-struct-15]
# COSE_Untagged_Message = COSE_Sign / COSE_Sign1 / COSE_Encrypt / COSE_Encrypt0 / COSE_Mac / COSE_Mac0

assert cose.tag == 18
protected, unprotected, payload, signature = cose.value

print("Protected=")
print(cbor.loads(protected))
print("")

print("Unprotected=")
print(unprotected)
print("")

# See https://www.iana.org/assignments/cwt/cwt.xhtml:
print(cbor.loads(payload))

cbor_payload = cbor.loads(payload)

import json

print(json.dumps(cbor_payload[-260], indent=2))

# breakpoint()
