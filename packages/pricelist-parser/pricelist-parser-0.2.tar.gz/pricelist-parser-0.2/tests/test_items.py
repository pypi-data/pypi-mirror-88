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


def test_arbitrary_attrs_passing():
    item = PricelistParserItem(sku='12-ппп', price=1234, randomattr='Я абсолютно случаен', anotherrandomattr=777)

    assert item.sku == '12-ппп'
    assert item.price == 1234
    assert item.randomattr == 'Я абсолютно случаен'
    assert item.anotherrandomattr == 777


def test_asdict():
    item = PricelistParserItem(sku='12-ппп', price=1234, randomattr='Я абсолютно случаен', anotherrandomattr=777)

    assert dict(item) == {'sku': '12-ппп', 'price': 1234, 'randomattr': 'Я абсолютно случаен', 'anotherrandomattr': 777}
