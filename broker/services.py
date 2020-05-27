import hashlib


def generate_signature(transaction, data):
    """generate signature to integrity check"""
    if not isinstance(data, dict):
        raise ValueError
    value = ';'.join([v for _, v in sorted(data.items())])
    value = transaction + ':' + value
    h = hashlib.sha256(value.encode())
    return h.hexdigest()
