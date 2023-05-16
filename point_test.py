from unittest import TestCase
from ecc import FieldElement
from point import Point
from s256point import N, S256Point, G
from signature import Signature
from hashlib import sha256
from private_key import PrivateKey


class ECCTest(TestCase):
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))

        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)

        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = (
            ((170, 142), (60, 139), (220, 181)),
            ((47, 71), (17, 56), (215, 68)),
            ((143, 98), (76, 66), (47, 71))
        )
        for points in valid_points:
            first_point = points[0]
            second_point = points[1]
            result = points[2]

            x1 = FieldElement(first_point[0], prime)
            y1 = FieldElement(first_point[1], prime)
            point1 = Point(x1, y1, a, b)

            x2 = FieldElement(second_point[0], prime)
            y2 = FieldElement(second_point[1], prime)
            point2 = Point(x2, y2, a, b)

            x3 = FieldElement(result[0], prime)
            y3 = FieldElement(result[1], prime)
            result_point = Point(x3, y3, a, b)

            self.assertEqual(point1 + point2, result_point)

    def test_add_infinity_point(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x1 = FieldElement(170, prime)
        y1 = FieldElement(142, prime)
        point = Point(x1, y1, a, b)

        self.assertEqual(point + Point(None, None, a, b), Point(x1, y1, a, b))
        self.assertEqual(Point(None, None, a, b) + point, Point(x1, y1, a, b))

    def test_on_bitcoin_group(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        p = 2**256 - 2**32 - 977
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        x = FieldElement(gx, p)
        y = FieldElement(gy, p)
        a = FieldElement(0, p)
        b = FieldElement(7, p)
        G = Point(x, y, a, b)

        self.assertEqual(n*G, Point(None, None, a, b))

    def test_g(self):
        self.assertEqual(N*G, S256Point(None, None))

    def test_signature(self):
        sig = Signature(
            0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )
        msgHash = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
        px = 0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574
        py = 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4
        point = S256Point(px, py)
        self.assertEqual(point.verify(msgHash, sig), True)

    def test_signing(self):
        e = 12345
        str = 'Programming Bitcoin!'
        msgHash = int(sha256(str.encode('utf-8')).hexdigest(), 16)
        k = 1234567890
        R = k * G
        r = R.x.num
        s = (msgHash + (r * e)) * pow(k, N - 2, N) % N
        signature = Signature(r, s)
        point = e * G
        self.assertEqual(point.verify(msgHash, signature), True)

    def test_pk_random(self):
        e = 12345
        pk = PrivateKey(e)

        str = 'Programming Bitcoin!'
        msgHash = int(sha256(str.encode('utf-8')).hexdigest(), 16)

        signature = pk.sign(msgHash)
        signature2 = pk.sign(msgHash)
        self.assertEqual(signature, signature2)

    def test_pk(self):
        e = 12345
        pk = PrivateKey(e)

        str = 'Programming Bitcoin!!!'
        msgHash = int(sha256(str.encode('utf-8')).hexdigest(), 16)

        signature = pk.sign(msgHash)
        self.assertTrue(pk.point.verify(msgHash, signature))

    def test_compressed_sec_format(self):
        e = 0xdeadbeef54321
        pk = PrivateKey(e)

        public_key = pk.point
        compressed_sec_format = public_key.sec(True)
        self.assertEqual(compressed_sec_format.hex(
        ), '0296be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe77690')

    def test_uncompressed_sec_format(self):
        e = 0xdeadbeef12345
        pk = PrivateKey(e)

        public_key = pk.point
        uncompressed_sec_format = public_key.sec(False)
        self.assertEqual(uncompressed_sec_format.hex(
        ), '04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121')

    def test_der_for_signature(self):
        signature = Signature(
            0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,
            0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        )

        der = signature.der()
        self.assertEqual(
            der.hex(),
            '3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec'
        )
