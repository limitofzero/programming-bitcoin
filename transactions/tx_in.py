from helpers.variant import read_varint
from helpers.little_endian_to_int import little_endian_to_int
from script.script import Script


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:  # <1>
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse(cls, stream):
        prev_tx = stream.read(32)[::-1]
        prev_index_bytes = stream.read(4)
        prev_index = little_endian_to_int(prev_index_bytes)
        script_sig = Script.parse(stream)
        sequence = little_endian_to_int(stream.read(4))
        return TxIn(prev_tx, prev_index, script_sig, sequence)
