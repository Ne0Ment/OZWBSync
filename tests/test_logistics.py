
from python.logistics import CategoryStock, Stock
from python.serializers import CategoryStockSerializer


stock1 = Stock('62', 'red', 123)
stock2 = Stock('62', 'red', 123)
stock3 = Stock('62', 'white', 123)

category_stock1 = CategoryStock('Футболки', [stock1, stock2])
category_stock2 = CategoryStock('Футболки', [stock1, stock2])
category_stock3 = CategoryStock('Футболки', [stock1, stock2, stock3])

css = CategoryStockSerializer()


def test_equality():
    assert stock1 == stock2
    assert category_stock1 == category_stock2


def test_inequality():
    assert stock1 != stock3
    assert category_stock1 != category_stock3


def test_serializalization():
    assert css.serialize(category_stock1) == css.serialize(category_stock2)
    assert css.serialize(category_stock1) != css.serialize(category_stock3)
