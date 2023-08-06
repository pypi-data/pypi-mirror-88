import os
import pytest

from pricelist_parser import CsvExtruder, Extruder, PricelistParser, XlsExtruder, XlsxExtruder


@pytest.fixture()
def single_header_definition():
    return [
        {
            'row': 5,
            'headers': [
                {
                    'column': 3,
                    'name': 'Артикул',
                    'type': 'sku',
                },
                {
                    'column': 4,
                    'name': 'Цена',
                    'type': 'price',
                },
            ],
        },
    ]


@pytest.fixture()
def multiple_headers_definition():
    return [
        {
            'row': 5,
            'headers': [
                {
                    'column': 3,
                    'name': 'Артикул',
                    'type': 'sku',
                },
                {
                    'column': 4,
                    'name': 'Цена',
                    'type': 'price',
                },
            ],
        },
        {
            'row': 17,
            'headers': [
                {
                    'column': 6,
                    'name': 'Артикул',
                    'type': 'sku',
                },
                {
                    'column': 4,
                    'name': 'Цена',
                    'type': 'price',
                },
                {
                    'column': 20,
                    'name': 'Размеры',
                    'type': 'dimensions',
                },
            ],
        },
        {
            'row': 11,
            'headers': [
                {
                    'column': 6,
                    'name': 'Я не знаю',
                    'type': None,
                },
                {
                    'column': 7,
                    'name': 'Что здесь',
                    'type': None,
                },
                {
                    'column': 8,
                    'name': 'За поля',
                    'type': None,
                },
                {
                    'column': 9,
                    'name': 'Такие',
                    'type': None,
                },
            ],
        },
    ]


@pytest.fixture()
def current_path():
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def sample_xls_ws(current_path):
    def _sample_xls_ws(worksheet_name='Лист с данными'):
        extruder = XlsExtruder()
        wb = extruder.load_file(current_path + '/samples/sample.xls')
        return extruder.get_worksheet(wb, worksheet_name)

    return _sample_xls_ws


@pytest.fixture()
def sample_xlsx_ws(current_path):
    def _sample_xlsx_ws(worksheet_name='Лист с данными'):
        extruder = XlsxExtruder()
        wb = extruder.load_file(current_path + '/samples/sample.xlsx')
        return extruder.get_worksheet(wb, worksheet_name)

    return _sample_xlsx_ws


@pytest.fixture()
def sample_csv_ws(current_path):
    def _sample_csv_ws():
        extruder = CsvExtruder()
        wb = extruder.load_file(current_path + '/samples/sample.csv')
        return extruder.get_worksheet(wb)

    return _sample_csv_ws


@pytest.fixture()
def parser():
    return PricelistParser()


@pytest.fixture()
def extruder():
    return Extruder()
