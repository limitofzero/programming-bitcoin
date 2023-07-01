from unittest import TestCase
from script.script import Script
from helpers.variant import encode_varint
import io


class ScriptTest(TestCase):
    def parsing_test(self):
        script_hex = '6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a'
        result = '3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01 0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a'

        hex_bytes = bytes.fromhex(script_hex)
        stream = io.BytesIO(hex_bytes)
        script = Script.parse(stream)
        self.assertEqual(script.__repr__(), result)

    def unlock_script_pubkey(self):
        script_pubkey = '767695935687'
        as_bytes = bytes.fromhex(script_pubkey)
        length = len(as_bytes)
        as_bytes = encode_varint(length) + as_bytes
        stream = io.BytesIO(as_bytes)
        script_pubkey_parsed = Script.parse(stream)

        b = 2
        script_sig = Script([
            b.to_bytes(1, 'big')
        ])
        result_script = script_sig + script_pubkey_parsed
        self.assertEqual(result_script.evaluate(''), True)
