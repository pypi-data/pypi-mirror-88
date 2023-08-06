import pytest

from pricelist_parser import PricelistParserItem


@pytest.mark.parametrize('sku, price, expected', [
    ['1123-ABC', 1233.1, True],
    ['', 1233.1, False],
    ['1123-ABC', None, False],
    [None, None, False],
])
def test_item_validate(sku, price, expected):
    item = PricelistParserItem(sku=sku, price=price)

    assert item.is_valid() is expected
