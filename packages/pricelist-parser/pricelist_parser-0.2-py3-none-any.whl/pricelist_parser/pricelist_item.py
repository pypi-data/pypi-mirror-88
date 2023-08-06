from price_parser import Price


class PricelistParserItem(object):
    def __init__(self, **kwargs):
        self.data = {}

        if 'sku' in kwargs:
            self.data['sku'] = self._process_as_string(kwargs.pop('sku'))

        if 'price' in kwargs:
            self.data['price'] = Price.fromstring(str(kwargs.pop('price'))).amount_float

        self.data = {**self.data, **kwargs}

    def keys(self):
        return self.data.keys()

    def __getattr__(self, name):
        if name in self.data.keys():
            return self.data[name]

    def __getitem__(self, key):
        return self.data[key]

    @staticmethod
    def _process_as_string(value):
        return str(value).strip()

    @staticmethod
    def _process_as_number(value):
        return float(value)

    def is_valid(self):
        if 'price' not in self.data.keys() or self.data['price'] is None:
            return False

        if 'sku' not in self.data.keys() or len(self.data['sku']) == 0:
            return False

        return True
