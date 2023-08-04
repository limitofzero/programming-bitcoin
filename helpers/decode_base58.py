from helpers.crypto.hash256 import hash256
from helpers.encode_base_58 import BASE58_ALPHABET


def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    #  last 4 characters
    checksum = combined[-4:]
    # [:-4] - up to last 4 characters
    # [:4] - 4 first characters
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum,
                                                     hash256(combined[:-4])[:4]))
    return combined[1:-4]
