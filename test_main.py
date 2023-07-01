import point_test
from script.script_test import ScriptTest
from transactions.tx_fetcher_test import TxFetcherTest
import transactions.tx_test
# from script.script_test import ScriptTest
# from transactions.tx_fetcher_test import TxFetcherTest
from helper import run

run(point_test.ECCTest('test_on_curve'))
run(point_test.ECCTest('test_add'))
run(point_test.ECCTest('test_add_infinity_point'))
run(point_test.ECCTest('test_on_bitcoin_group'))
run(point_test.ECCTest('test_g'))
run(point_test.ECCTest('test_signature'))
run(point_test.ECCTest('test_signing'))
run(point_test.ECCTest('test_pk_random'))
run(point_test.ECCTest('test_pk'))
run(point_test.ECCTest('test_compressed_sec_format'))
run(point_test.ECCTest('test_uncompressed_sec_format'))
run(point_test.ECCTest('test_der_for_signature'))
run(point_test.ECCTest('test_encode_base58'))
run(point_test.ECCTest('test_point_address_mainnet'))
run(point_test.ECCTest('test_wif_mainnet'))

run(transactions.tx_test.TxTest('parsing_test'))
run(transactions.tx_test.TxTest('tx_parse_modern_tx'))
run(transactions.tx_test.TxTest('tx_calculate_fee'))
#
run(ScriptTest('unlock_script_pubkey'))

# run(TxFetcherTest('fetch_mainnet_tx_by_hash_test'))
