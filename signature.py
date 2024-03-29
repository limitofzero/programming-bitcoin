from io import BytesIO


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

    @classmethod
    def parse(cls, signature_bin):
        if len(signature_bin) == 64:
            r = int.from_bytes(signature_bin[:32], 'big')
            s = int.from_bytes(signature_bin[32:], 'big')
            return cls(r, s)

        s = BytesIO(signature_bin)
        compound = s.read(1)[0]
        if compound != 0x30:
            raise SyntaxError("Bad Signature")
        length = s.read(1)[0]
        if length + 2 != len(signature_bin):
            raise SyntaxError("Bad Signature Length")
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        rlength = s.read(1)[0]
        r = int.from_bytes(s.read(rlength), 'big')
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        slength = s.read(1)[0]
        s = int.from_bytes(s.read(slength), 'big')
        if len(signature_bin) != 6 + rlength + slength:
            raise SyntaxError("Signature too long")
        return cls(r, s)
