import hashlib


def hash160(val):
    return hashlib.new('ripemd160', hashlib.sha256(val).digest()).digest()
