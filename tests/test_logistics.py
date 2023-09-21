
from python.logistics import RawProduct


raw_product1 = RawProduct('bebra', '62', 'red', 123)
raw_product2 = RawProduct('bebra', '62', 'red', 123)
raw_product3 = RawProduct('bebra', '62', 'white', 123)


def test_equality():
    assert raw_product1 == raw_product2


def test_inequality():
    assert raw_product1 != raw_product3
