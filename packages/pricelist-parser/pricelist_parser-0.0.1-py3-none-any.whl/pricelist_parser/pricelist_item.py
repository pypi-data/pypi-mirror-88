from price_parser import Price


class PricelistParserItem(object):
    def __init__(self, sku, price, name=None, category=None):
        self.sku = str(sku).strip()
        self.price = Price.fromstring(str(price)).amount_float

    def is_valid(self):
        if self.price is None:
            return False

        if len(self.sku) == 0:
            return False

        return True
