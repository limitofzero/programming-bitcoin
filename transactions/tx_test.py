from unittest import TestCase
from unittest.mock import patch
import io
from s256point import S256Point
from script.p2pkh_script import p2pkh_script
from script.script import Script
from signature import Signature
from transactions.tx import SIGHASH_ALL, SIGHASH_ALL_BYTES, Tx
from transactions.tx_out import TxOut
from transactions.tx_in import TxIn
from transactions.tx_fetcher import TxFetcher
from helpers.decode_base58 import decode_base58

from private_key import PrivateKey


class TxTest(TestCase):
    def parsing_test(self):
        tx = """010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e0100
    00006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951
    c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0
    da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4
    038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a473044022078
    99531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b84
    61cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba
    1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c35
    6efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da
    6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c3
    4210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49
    abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd
    04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea833
    1ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c
    2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20df
    e7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948
    a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46
    430600
"""
        hex_bytes = bytes.fromhex(tx)
        stream = io.BytesIO(hex_bytes)
        tx = Tx.parse(stream)
        script_sig_of_second_input = """304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a71601 035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937"""
        self.assertEqual(tx.tx_ins[1].script_sig.__repr__(),
                         script_sig_of_second_input)

        expected_script_pubkey = """OP_DUP OP_HASH160 ab0c0b2e98b1ab6dbf67d4750b0a56244948a879 OP_EQUALVERIFY OP_CHECKSIG"""
        self.assertEqual(
            tx.tx_outs[0].script_pubkey.__repr__(), expected_script_pubkey)

    def tx_parse_modern_tx(self):
        tx = """010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff5f03ba240c182f5669614254432f4d696e6564206279207764777764772f2cfabe6d6dd64f1cd18c51a6351b58b537b8046cc7896ca8238b349c7172a59e27bec9528410000000000000001040885a02583061024e2058d6c3bb020000000000ffffffff034e00ef25000000001976a914536ffa992491508dca0354e52f32a3a7a679a53a88ac00000000000000002b6a2952534b424c4f434b3aa6872e2d071565ca2e070c34cedc67e771970dc7558ac85faf0997240052ae250000000000000000266a24aa21a9edbb4abe6f71080b0983d1b489bbbaccd87c782a85d93944ae7246b665e27dfba90120000000000000000000000000000000000000000000000000000000000000000000000000"""
        hex_bytes = bytes.fromhex(tx)
        tx = Tx.parse_raw_tx(hex_bytes)

        self.assertEqual(
            tx.id(), '6530b6ed99c401262c4d40b2d097ec0fd28091b6e8b4b30e04b6b6d82576d17b'
        )

    def tx_calculate_fee(self):
        tx = """02000000018c6bc2f8f12d6b6c4a5bdbaa589696f9944fabc3a778e6d59afdccfc6744426a010000006b483045022100b40fe87efb5df7f477d8b950e0ebace4ab3f8c9fc75161d1cf9919e0e03a685402207d4fffec4d716f921f2f1b3a82b485dfe552928638948c42c4e6f33356033b3b012103299a44cd9b024d6fbcdaaaf3dc3ebf15e426cc6ca23d2b14789cc54d30feb0b0fdffffff02a41f3200000000001976a914e41f238e7b261d76f967b76af24c86a86e30adf988ac57084501000000001976a914c95eeef328d053591ff7a6a298314ce29d657bfa88ac00000000"""
        hex_bytes = bytes.fromhex(tx)
        tx = Tx.parse_raw_tx(hex_bytes)

        self.assertEqual(
            tx.fee(), 76400
        )

    def tx_validation(self):
        bytes_tx = bytes.fromhex(
            '02000000018c6bc2f8f12d6b6c4a5bdbaa589696f9944fabc3a778e6d59afdccfc6744426a010000006b483045022100b40fe87efb5df7f477d8b950e0ebace4ab3f8c9fc75161d1cf9919e0e03a685402207d4fffec4d716f921f2f1b3a82b485dfe552928638948c42c4e6f33356033b3b012103299a44cd9b024d6fbcdaaaf3dc3ebf15e426cc6ca23d2b14789cc54d30feb0b0fdffffff02a41f3200000000001976a914e41f238e7b261d76f967b76af24c86a86e30adf988ac57084501000000001976a914c95eeef328d053591ff7a6a298314ce29d657bfa88ac00000000')
        tx = Tx.parse(io.BytesIO(bytes_tx))

        script_sig = tx.tx_ins[0].script_sig.cmds[1]
        publik_key = S256Point.parse(script_sig)

        sig = Signature.parse(tx.tx_ins[0].script_sig.cmds[0][:-1])
        z = tx.sig_hash(0)

        self.assertTrue(
            publik_key.verify(z, sig)
        )

    def tx_validate_input(self):
        bytes_tx = bytes.fromhex(
            '02000000018c6bc2f8f12d6b6c4a5bdbaa589696f9944fabc3a778e6d59afdccfc6744426a010000006b483045022100b40fe87efb5df7f477d8b950e0ebace4ab3f8c9fc75161d1cf9919e0e03a685402207d4fffec4d716f921f2f1b3a82b485dfe552928638948c42c4e6f33356033b3b012103299a44cd9b024d6fbcdaaaf3dc3ebf15e426cc6ca23d2b14789cc54d30feb0b0fdffffff02a41f3200000000001976a914e41f238e7b261d76f967b76af24c86a86e30adf988ac57084501000000001976a914c95eeef328d053591ff7a6a298314ce29d657bfa88ac00000000')
        tx = Tx.parse(io.BytesIO(bytes_tx))
        self.assertTrue(
            tx.verify_input(0, True)
        )

    def tx_verify(self):
        bytes_tx = bytes.fromhex(
            '02000000018c6bc2f8f12d6b6c4a5bdbaa589696f9944fabc3a778e6d59afdccfc6744426a010000006b483045022100b40fe87efb5df7f477d8b950e0ebace4ab3f8c9fc75161d1cf9919e0e03a685402207d4fffec4d716f921f2f1b3a82b485dfe552928638948c42c4e6f33356033b3b012103299a44cd9b024d6fbcdaaaf3dc3ebf15e426cc6ca23d2b14789cc54d30feb0b0fdffffff02a41f3200000000001976a914e41f238e7b261d76f967b76af24c86a86e30adf988ac57084501000000001976a914c95eeef328d053591ff7a6a298314ce29d657bfa88ac00000000')
        tx = Tx.parse(io.BytesIO(bytes_tx))
        self.assertTrue(
            tx.verify(True)
        )

    @patch('transactions.tx_fetcher.TxFetcher.fetch', return_value=None)
    def tx_sign_input(self, mock_fetch):
        prev_tx = bytes.fromhex(
            '0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
        prev_index = 13
        tx_in = TxIn(prev_tx, prev_index)
        change_amount = int(0.33*100000000)
        change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
        change_script = p2pkh_script(change_h160)
        change_output = TxOut(amount=change_amount,
                              script_pubkey=change_script)
        target_amount = int(0.1*100000000)
        target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
        target_script = p2pkh_script(target_h160)
        target_output = TxOut(amount=target_amount,
                              script_pubkey=target_script)
        tx_obj = Tx(1, [tx_in], [change_output, target_output], 0, True)

        mockedTxOutList = [TxOut(int(0.1*100000000), None) for i in range(15)]
        mockedTxOutList[13] = TxOut(
            int(0.44*100000000),
            p2pkh_script(change_h160)
        )
        mockedPrevTx = Tx(1, [], mockedTxOutList, 0, True)
        mock_fetch.return_value = mockedPrevTx

        private_key = PrivateKey(secret=8675309)

        self.assertTrue(tx_obj.sign_input(0, private_key, True))
