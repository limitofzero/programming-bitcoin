VALUE_MARKER = 2


def pack_value_to_der(val):
    rbin = val.to_bytes(32, byteorder='big')
    rbin = rbin.lstrip(b'\x00')
    if rbin[0] & 0x80:
        rbin = b'\x00' + rbin
    return bytes([VALUE_MARKER, len(rbin)]) + rbin


class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

    def __eq__(self, other):
        return self.r == other.r and self.s == other.s

    def der(self):
        rbin = pack_value_to_der(self.r)
        sbin = pack_value_to_der(self.s)
        result = rbin + sbin
        return bytes([0x30, len(result)]) + result
