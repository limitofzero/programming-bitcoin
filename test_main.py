import point_test
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
