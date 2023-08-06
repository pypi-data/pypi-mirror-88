import pytest

from pricelist_parser import parse_pricelist


@pytest.mark.parametrize('path, expected', [
    ['/samples/price_list_1.xls', 'xls'],
    ['/samples/price_list_1.xlsx', 'xlsx'],
    ['/samples/price_list_1.csv', 'csv'],
    ['/samples/price_list_1.avi', 'avi'],
])
def test_detect_file_type(path, expected, parser):
    detected_file_type = parser.detect_file_type(path)

    assert detected_file_type == expected


@pytest.mark.parametrize('path, expected', [
    ['/samples/price_list_1.xls', 'price_list_1'],
    ['/samples/price_list_1 или 2.xlsx', 'price_list_1 или 2'],
    ['/samples/price_list_1.version.2.1.4.csv', 'price_list_1.version.2.1.4'],
    ['/samples/.csv', '.csv'],
])
def test_get_slug_from_path(path, expected, parser):
    detected_file_type = parser.get_slug_from_path(path)

    assert detected_file_type == expected


def test_parse_pricelist_xls(current_path, parser):
    parser.add_data_source(source_file=current_path + '/samples/sample.xls', slug='sample')

    assert len(parser.data_sources['sample'].items) == 679


def test_parse_pricelist_xlsx(current_path, parser):
    parser.add_data_source(source_file=current_path + '/samples/sample.xlsx', slug='sample')

    assert len(parser.data_sources['sample'].items) == 679


def test_parse_pricelist_csv(current_path, parser):
    parser.add_data_source(source_file=current_path + '/samples/sample.csv', slug='sample')

    assert len(parser.data_sources['sample'].items) == 4


def test_parse_pricelist_undefined(current_path, parser):
    try:
        parser.add_data_source(source_file=current_path + '/samples/sample.doc', slug='sample')

        raise AssertionError()
    except ValueError:
        assert True


def test_parse_pricelist_function(current_path):
    items = parse_pricelist(current_path + '/samples/sample.xls')

    assert len(items) == 679


def test_passing_all_extruded_values(current_path):
    items = parse_pricelist(current_path + '/samples/sample.xls')

    assert items[0].sku == '123-ААА'
    assert items[0].description == 'Сепулька обычная недеформированная'
    assert items[0].dimensions == '134x34'
    assert items[0].price == 3999.99


def test_extra_header_signatures(current_path, parser):
    parser.add_data_source(current_path + '/samples/sample.xls', header_signatures={'title': ['заголовок']})

    assert 'title' in parser.data_sources['sample'].items[0].keys()
    assert parser.data_sources['sample'].items[0].title == 'Здесь нужно что-то написать'


def test_extra_header_signatures_in_parse_pricelist_function(current_path):
    items = parse_pricelist(current_path + '/samples/sample.xls', header_signatures={'title': ['заголовок']})

    assert 'title' in items[0].keys()
    assert items[0].sku == '123-ААА'
    assert items[0].title == 'Здесь нужно что-то написать'


def test_replace_header_signatures_in_parse_pricelist_function(current_path):
    items = parse_pricelist(current_path + '/samples/sample.xls', header_signatures={'sku': ['заголовок']})

    assert items[0].sku == 'Здесь нужно что-то написать'
