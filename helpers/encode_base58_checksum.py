from helpers.crypto.hash256 import hash256
from helpers.encode_base_58 import encode_base58


def encode_base58_checksum(b):
    hash = hash256(b)
    return encode_base58(b + hash[:4])
