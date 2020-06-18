from json import JSONEncoder

from decimal import Decimal


class DecimalEncoder(JSONEncoder):

    def default(self, o):  # noqa
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)
