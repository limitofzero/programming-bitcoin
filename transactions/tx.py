from helpers.crypto.hash256 import hash256
from helpers.little_endian_to_int import int_to_little_endian, little_endian_to_int
from helpers.variant import encode_varint, read_varint
from transactions.tx_in import TxIn
from transactions.tx_out import TxOut


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )

    def id(self):  # <3>
        '''Human-readable hexadecimal of the transaction hash'''
        return self.hash().hex()

    def hash(self):  # <4>
        '''Binary hash of the legacy serialization'''
        return hash256(self.serialize())[::-1]

    def serialize(self):
        '''Returns the byte serialization of the transaction'''
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

    @classmethod
    def parse(cls, stream, testnet=False):
        version = little_endian_to_int(stream.read(4))
        tx_ins_count = read_varint(stream)
        tx_ins = []
        for i in range(tx_ins_count):
            tx = TxIn.parse(stream)
            tx_ins.append(tx)

        tx_outs = []
        tx_out_count = read_varint(stream)
        for i in range(tx_out_count):
            tx_outs.append(TxOut.parse(stream))

        locktime = little_endian_to_int(stream.read(4))
        return Tx(version, tx_ins, tx_outs, locktime)
