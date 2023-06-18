def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(val, length):
    return val.to_bytes(length, 'little')
