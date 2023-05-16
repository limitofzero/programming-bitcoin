from point import Point
from s256field import P, S256Field

A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x, y, a, b)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, msgHash, signature):
        # U = message * s^(-1) % N
        # V = r * s^(-1) % N
        # PublicKey = G * PrivateKey
        # C = U * G + V * PublicKey
        # if C.x % N == r
        s_inv = pow(signature.s, N - 2, N)
        u = msgHash * s_inv % N
        v = signature.r * s_inv % N
        c = u * G + v * self
        return c.x.num == signature.r

    def sec(self, compressed=True):
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') \
                + self.y.num.to_bytes(32, 'big')

    @classmethod
    def parse(self, sec_bin):
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x, y)
        else:
            x = S256Field(int.from_bytes(sec_bin[1:33], 'big'))
            is_even = sec_bin[0] == 2
            alpha = x ** 3 + S256Field(B)
            beta = alpha.sqrt()
            if beta % 2 == 0:
                even_beta = beta
                odd_beta = S256Field(P - beta)
            else:
                even_beta = S256Field(P - beta)
                odd_beta = beta
            if is_even:
                return S256Point(x, even_beta)
            return S256Point(x, odd_beta)


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)
