from unittest import TestCase
import io
from transactions.tx import Tx
from transactions.tx_fetcher import TxFetcher


class TxFetcherTest(TestCase):
    def fetch_mainnet_tx_by_hash_test(self):
        tx_id = '1580adc1a981d57e97052a7b2ecdeefe520014a9d5b1d69d208c4cf6d566eb36'
        tx = TxFetcher.fetch(tx_id, False)
        self.assertEqual(tx.id() == tx_id)
