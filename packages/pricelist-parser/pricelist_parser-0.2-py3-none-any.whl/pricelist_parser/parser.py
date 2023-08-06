from os.path import basename, splitext

from .extruders import CsvExtruder, XlsExtruder, XlsxExtruder


class PricelistParser(object):
    def __init__(self):
        self.data_sources = {}

    def add_data_source(self, source_file, slug=None, header_signatures=None, replace_header_signatures=False, **kwargs):
        file_type = self.detect_file_type(path=source_file)

        if file_type == 'xls':
            extruder = XlsExtruder(source_file, **kwargs)
        elif file_type == 'xlsx':
            extruder = XlsxExtruder(source_file, **kwargs)
        elif file_type == 'csv':
            extruder = CsvExtruder(source_file, **kwargs)
        else:
            raise ValueError(f'Unsupported file type {file_type}. Please use one of xls, xlsx or csv instead')

        if slug is None:
            slug = self.get_slug_from_path(path=source_file)

        if header_signatures is not None:
            extruder.update_header_signatures(signatures=header_signatures, replace=replace_header_signatures)

        self.data_sources[slug] = extruder.load_data(**kwargs)

        return self.data_sources[slug]

    @staticmethod
    def detect_file_type(path):
        file_type = splitext(path)[1]

        if file_type is not None:
            return str(file_type).lstrip('.')
        else:
            return None

    @staticmethod
    def get_slug_from_path(path):
        return splitext(basename(path))[0]


def parse_pricelist(pricelist_file, **kwargs):
    parser = PricelistParser()
    parser.add_data_source(source_file=pricelist_file, slug='default', **kwargs)

    return parser.data_sources['default'].items
