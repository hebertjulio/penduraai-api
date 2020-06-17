from json import JSONEncoder

from decimal import Decimal


class DecimalEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)
