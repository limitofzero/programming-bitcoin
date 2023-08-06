import copy
from io import BytesIO
from helpers.crypto.hash256 import hash256
from helpers.little_endian_to_int import int_to_little_endian, little_endian_to_int
from helpers.variant import encode_varint, read_varint
from script.script import Script
from transactions.tx_in import TxIn
from transactions.tx_out import TxOut

SIGHASH_ALL = 1
SIGHASH_ALL_BYTES = int_to_little_endian(SIGHASH_ALL, 4)


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

    @classmethod
    def parse_raw_tx(cls, raw, testnet=False):
        if raw[4] == 0:
            raw = raw[:4] + raw[6:]
            tx = cls.parse(BytesIO(raw), testnet=testnet)
            tx.locktime = little_endian_to_int(raw[-4:])
        else:
            tx = cls.parse(BytesIO(raw), testnet=testnet)
        return tx

    def fee(self):
        input_amount = 0
        for tx_in in self.tx_ins:
            input_amount += tx_in.value()
        output_amount = 0
        for tx_out in self.tx_outs:
            output_amount += tx_out.amount

        fee = input_amount - output_amount
        if fee < 0:
            raise ValueError('Fee is negative: {}'.format(fee))

        return fee

    def sig_hash(self, tx_in_index, testnet=False):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for index, tx_in in enumerate(self.tx_ins):
            if index == tx_in_index:
                result += TxIn(
                    tx_in.prev_tx,
                    tx_in.prev_index,
                    tx_in.script_pubkey(testnet),
                    tx_in.sequence
                ).serialize()
            else:
                result += TxIn(
                    tx_in.prev_tx,
                    tx_in.prev_index,
                    Script(),
                    tx_in.sequence
                ).serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        result += SIGHASH_ALL_BYTES
        hash = hash256(result)
        z = int.from_bytes(hash, 'big')
        return z

    def sign_input(self, in_index, pk, testnet=False):
        z = self.sig_hash(in_index, testnet)
        der = pk.sign(z).der()
        signature = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = pk.point.sec()
        self.tx_ins[in_index].script_sig = Script([signature, sec])
        return self.verify_input(in_index, True, testnet)

    def verify_input(self, input_index, fix_sig_length=False, testnet=False):
        tx_in = self.tx_ins[input_index]
        script = tx_in.script_sig + tx_in.script_pubkey(testnet)
        z = self.sig_hash(input_index, testnet)
        return script.evaluate(z, fix_sig_length)

    def verify(self, fix_sig_length=False):
        if self.fee() < 0:
            return False

        for i in range(len(self.tx_ins)):
            if not self.verify_input(i, fix_sig_length):
                return False
        return True
