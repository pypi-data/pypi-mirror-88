import pytest

from pricelist_parser import PricelistParser, parse_pricelist


@pytest.mark.parametrize('path, expected', [
    ['/samples/price_list_1.xls', 'xls'],
    ['/samples/price_list_1.xlsx', 'xlsx'],
    ['/samples/price_list_1.csv', 'csv'],
    ['/samples/price_list_1.avi', 'avi'],
])
def test_detect_file_type(path, expected):
    parser = PricelistParser()

    detected_file_type = parser.detect_file_type(path)

    assert detected_file_type == expected


@pytest.mark.parametrize('path, expected', [
    ['/samples/price_list_1.xls', 'price_list_1'],
    ['/samples/price_list_1 или 2.xlsx', 'price_list_1 или 2'],
    ['/samples/price_list_1.version.2.1.4.csv', 'price_list_1.version.2.1.4'],
    ['/samples/.csv', '.csv'],
])
def test_get_slug_from_path(path, expected):
    parser = PricelistParser()

    detected_file_type = parser.get_slug_from_path(path)

    assert detected_file_type == expected


def test_parse_pricelist_xls(current_path):
    parser = PricelistParser()
    parser.add_data_source(source_file=current_path + '/samples/sample.xls', slug='sample')

    assert len(parser.data_sources['sample'].items) == 679


def test_parse_pricelist_xlsx(current_path):
    parser = PricelistParser()
    parser.add_data_source(source_file=current_path + '/samples/sample.xlsx', slug='sample')

    assert len(parser.data_sources['sample'].items) == 679


def test_parse_pricelist_csv(current_path):
    parser = PricelistParser()
    parser.add_data_source(source_file=current_path + '/samples/sample.csv', slug='sample')

    assert len(parser.data_sources['sample'].items) == 4


def test_parse_pricelist_undefined(current_path):
    parser = PricelistParser()

    try:
        parser.add_data_source(source_file=current_path + '/samples/sample.doc', slug='sample')

        raise AssertionError()
    except ValueError:
        assert True


def test_parse_pricelist_function(current_path):
    items = parse_pricelist(current_path + '/samples/sample.xls')

    assert len(items) == 679
