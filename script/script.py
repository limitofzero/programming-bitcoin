from helpers.variant import read_varint


class Script:
    def __init__(self, signature=None, pubkey=None):
        self.signature = signature
        self.pubkey = pubkey

    def __repr__(self):
        return '{} {}'.format(
            self.signature.hex(),
            self.pubkey.hex(),
        )

    @classmethod
    def parse(cls, s):
        length = s.read(1)[0]  # read length of the entire script
        length_sig = s.read(1)[0]  # read length of the signature
        signature = s.read(length_sig)
        pubkey_len = s.read(1)[0]  # read length of the public key
        pubkey = s.read(pubkey_len)  # read the public key
        return cls(signature, pubkey)  # return a new Script object
