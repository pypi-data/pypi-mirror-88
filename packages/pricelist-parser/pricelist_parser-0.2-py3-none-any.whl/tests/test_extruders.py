import openpyxl
import pytest
import xlrd

from pricelist_parser import CsvExtruder, Extruder, XlsExtruder, XlsxExtruder, parse_pricelist


def flatten_headers(headers):
    return {x['name']: x['column'] for x in headers['headers']}


@pytest.mark.parametrize('value, expected', [
    ['Цена', 'price'],
    ['Отпускная цена', 'price'],
    ['РРЦ', 'price'],
    ['Цена продажи', 'price'],
    ['Цена, руб.', 'price'],
    ['Отпускная цена (руб.) за 1 упаковку без НДС', 'price'],
    ['Цена в т.ч. НДС', 'price'],
    ['Розничная цена до скидки', 'price'],
    ['РЕКОМЕНДОВАННАЯ ЦЕНА', 'price'],
    ['Базовая цена', 'price'],
    ['штрих-коды', 'sku'],
    ['Артикул', 'sku'],
    ['Модель', 'sku'],
    ['Код', 'sku'],
    ['ПРАЙС-ЛИСТ', None],
    ['Кол-во в коробке', 'quantity'],
])
def test_detect_header_type(value, expected):
    extruder = Extruder()

    detected_type = extruder.detect_header_type(value)

    assert detected_type is expected


def test_detect_headers_random_xls(current_path):
    extruder = XlsExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xls')
    ws = extruder.get_worksheet(wb, 'Лист с заголовком')

    headers = extruder.detect_headers(ws)

    assert len(headers) == 0


def test_detect_headers_filled_xls(current_path):
    extruder = XlsExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xls')
    ws = extruder.get_worksheet(wb, 'Лист с заголовком')

    headers = extruder.detect_headers(ws)

    assert len(headers) == 0


def test_detect_headers_random_xlsx(current_path):
    extruder = XlsxExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xlsx')
    ws = extruder.get_worksheet(wb, 'Лист с заголовком')

    headers = extruder.detect_headers(ws)

    assert len(headers) == 0


def test_detect_headers_filled_xlsx(current_path):
    extruder = XlsxExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xlsx')
    ws = extruder.get_worksheet(wb, 'Лист с данными')

    headers = extruder.detect_headers(ws)

    assert len(headers) == 1
    assert flatten_headers(headers[0]) == {
        'Артикул': 2,
        'Описание': 3,
        'Просто заголовок': 4,
        'Размеры': 5,
        'Кол-во': 6,
        'Цена с НДС': 7,
        'Цена без НДС': 8,
        'Сумма': 9,
    }


def test_headers_map_filled_xlsx(current_path):
    extruder = XlsxExtruder(current_path + '/samples/sample.xlsx')
    extruder.load_data()

    headers_map = extruder.get_headers_map(extruder.loaded_file)

    assert len(headers_map) == 2
    assert headers_map[0]['worksheet'].title == 'Лист с данными'
    assert headers_map[1]['worksheet'].title == 'Лист с данными – 2'
    assert len(headers_map[0]['headers']['headers']) == 8


def test_headers_map_filled_xls(current_path):
    extruder = XlsExtruder(current_path + '/samples/sample.xls')
    extruder.load_data()

    headers_map = extruder.get_headers_map(extruder.loaded_file)

    assert len(headers_map) == 2
    assert headers_map[0]['worksheet'].name == 'Лист с данными'
    assert headers_map[1]['worksheet'].name == 'Лист с данными – 2'
    assert len(headers_map[0]['headers']['headers']) == 8


def test_extract_data_from_sheet_xlsx(current_path):
    extruder = XlsxExtruder(current_path + '/samples/sample.xlsx')
    extruder.load_data()

    headers_map = extruder.get_headers_map(extruder.loaded_file)
    items = extruder.extract_data_from_sheet(headers_map[0])

    assert len(items) == 9
    assert items[0].sku == '123-ААА'
    assert items[0].price == 3999.99

    assert items[8].sku == '324-ППП'
    assert items[8].price == 1150.6


def test_extract_data_from_sheet_xls(current_path):
    extruder = XlsExtruder(current_path + '/samples/sample.xls')
    extruder.load_data()

    headers_map = extruder.get_headers_map(extruder.loaded_file)
    items = extruder.extract_data_from_sheet(headers_map[0])

    assert len(items) == 9
    assert items[0].sku == '123-ААА'
    assert items[0].price == 3999.99

    assert items[8].sku == '324-ППП'
    assert items[8].price == 1150.6


def test_select_best_headers_single(single_header_definition):
    extruder = Extruder()

    headers = extruder.select_best_headers(single_header_definition)

    assert isinstance(headers, dict)
    assert headers['row'] == 5


def test_select_best_headers_multiple(multiple_headers_definition):
    extruder = Extruder()

    headers = extruder.select_best_headers(multiple_headers_definition)

    assert isinstance(headers, dict)
    assert headers['row'] == 17


def test_xls_load_file(current_path):
    extruder = XlsExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xls')

    assert type(wb) is xlrd.book.Book


def test_xls_get_worksheet_names(current_path):
    extruder = XlsExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xls')

    assert extruder.get_worksheet_names(wb) == ['Лист с заголовком', 'Лист с данными', 'Лист с данными – 2']


def test_xls_get_worksheet(sample_xls_ws):
    ws = sample_xls_ws('Лист с данными')

    assert ws.name == 'Лист с данными'


def test_xls_get_cols_num(sample_xls_ws):
    extruder = XlsExtruder()
    ws = sample_xls_ws('Лист с данными')

    assert extruder.get_cols_num(ws) == 9


def test_xls_get_rows_num(sample_xls_ws):
    extruder = XlsExtruder()
    ws = sample_xls_ws('Лист с данными')

    assert extruder.get_rows_num(ws) == 16


def test_xls_get_cell(sample_xls_ws):
    extruder = XlsExtruder()
    ws = sample_xls_ws('Лист с заголовком')

    assert extruder.get_cell(ws, 1, 1) == 'A1'
    assert extruder.get_cell(ws, 2, 2) == 'B2'
    assert extruder.get_cell(ws, 3, 3) == 'C3'


def test_xlsx_load_file(current_path):
    extruder = XlsxExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xlsx')

    assert type(wb) is openpyxl.workbook.workbook.Workbook


def test_xlsx_get_worksheet_names(current_path):
    extruder = XlsxExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.xlsx')

    assert extruder.get_worksheet_names(wb) == ['Лист с заголовком', 'Лист с данными', 'Лист с данными – 2']


def test_xlsx_get_worksheet(sample_xlsx_ws):
    ws = sample_xlsx_ws('Лист с данными')

    assert ws.title == 'Лист с данными'


def test_xlsx_get_cols_num(sample_xlsx_ws):
    extruder = XlsxExtruder()
    ws = sample_xlsx_ws('Лист с данными')

    assert extruder.get_cols_num(ws) == 9


def test_xlsx_get_rows_num(sample_xlsx_ws):
    extruder = XlsxExtruder()
    ws = sample_xlsx_ws('Лист с данными')

    assert extruder.get_rows_num(ws) == 16


def test_xlsx_get_cell(sample_xlsx_ws):
    extruder = XlsxExtruder()
    ws = sample_xlsx_ws('Лист с заголовком')

    assert extruder.get_cell(ws, 1, 1) == 'A1'
    assert extruder.get_cell(ws, 2, 2) == 'B2'
    assert extruder.get_cell(ws, 3, 3) == 'C3'


def test_csv_load_file(current_path):
    extruder = CsvExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.csv')

    assert type(wb) is CsvExtruder


def test_csv_get_worksheet_names(current_path):
    extruder = CsvExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.csv')

    assert extruder.get_worksheet_names(wb) == ['default']


def test_csv_get_worksheet_incorrect(current_path):
    extruder = CsvExtruder()
    wb = extruder.load_file(current_path + '/samples/sample.csv')

    extruder.get_worksheet(wb, 'every_other_name')


def test_csv_get_worksheet_correct(current_path):
    extruder = CsvExtruder()

    wb = extruder.load_file(current_path + '/samples/sample.csv')

    ws = extruder.get_worksheet(wb, 'default')

    assert type(ws) is CsvExtruder


def test_csv_get_cols_num(sample_csv_ws):
    extruder = CsvExtruder()
    ws = sample_csv_ws()

    assert extruder.get_cols_num(ws) == 8


def test_csv_get_rows_num(sample_csv_ws):
    extruder = CsvExtruder()
    ws = sample_csv_ws()

    assert extruder.get_rows_num(ws) == 13


def test_csv_get_cell(sample_csv_ws):
    extruder = CsvExtruder()
    ws = sample_csv_ws()

    assert extruder.get_cell(ws, 1, 1) == 'Артикул'
    assert extruder.get_cell(ws, 1, 2) == 'Сепульки обычные'
    assert extruder.get_cell(ws, 1, 3) == '123-ААА'

    assert extruder.get_cell(ws, 2, 1) == 'Описание'
    assert extruder.get_cell(ws, 3, 1) == 'Просто заголовок'
    assert extruder.get_cell(ws, 4, 1) == 'Размеры'


def test_wrong_encoding_exception_in_csv(current_path):
    extruder = CsvExtruder()

    try:
        extruder.load_file(current_path + '/samples/cp154_encoded.csv')

        raise AssertionError()
    except UnicodeDecodeError:
        assert True


def test_set_encoding_in_csv_load_file(current_path):
    extruder = CsvExtruder()
    extruder.load_file(current_path + '/samples/cp154_encoded.csv', encoding='cp154')

    assert True


def test_set_encoding_in_parse_pricelist_function(current_path):
    parse_pricelist(current_path + '/samples/cp154_encoded.csv', encoding='cp154')

    assert True


def test_default_header_signature_list(extruder):
    assert set(extruder.header_signatures.keys()) == {'sku', 'price', 'quantity', 'name', 'description', 'dimensions', 'weight', 'link', 'vat', 'order'}


def test_update_header_signature(extruder):
    extruder.update_header_signatures({'sku': ['товар', 'подношение', 'оброк']})

    assert 'товар' in extruder.header_signatures['sku']
    assert 'подношение' in extruder.header_signatures['sku']
    assert 'оброк' in extruder.header_signatures['sku']
    assert 'артикул' in extruder.header_signatures['sku']


def test_replace_header_signature(extruder):
    extruder.update_header_signatures({'sku': ['товар', 'подношение', 'оброк']}, replace=True)

    assert 'товар' in extruder.header_signatures['sku']
    assert 'подношение' in extruder.header_signatures['sku']
    assert 'оброк' in extruder.header_signatures['sku']
    assert 'артикул' not in extruder.header_signatures['sku']


def test_insert_header_signature(extruder):
    extruder.update_header_signatures({'flavour': ['lepton', 'baryon', 'strangeness', 'charm', 'bottom', 'topness']})

    assert 'flavour' in extruder.header_signatures.keys()
    assert set(extruder.header_signatures['flavour']) == {'lepton', 'baryon', 'strangeness', 'charm', 'bottom', 'topness'}

    assert 'sku' in extruder.header_signatures.keys()
    assert 'price' in extruder.header_signatures.keys()
    assert 'quantity' in extruder.header_signatures.keys()
    assert 'name' in extruder.header_signatures.keys()


def test_header_signatures_not_propagated():
    extruder_1 = Extruder()
    extruder_1.update_header_signatures({'flavour': ['lepton', 'baryon', 'strangeness', 'charm', 'bottom', 'topness']})

    extruder_2 = Extruder()

    assert 'flavour' in extruder_1.header_signatures.keys()
    assert 'flavour' not in extruder_2.header_signatures.keys()
