import hashlib


def generate_signature(transaction, payload):
    """generate signature to integrity check"""
    if not isinstance(payload, dict):
        raise ValueError
    value = ';'.join(v for _, v in sorted(payload.items()))
    value = transaction + ':' + value
    h = hashlib.sha256(value.encode())
    return h.hexdigest()
