import hashlib


def generate_signature(payload):
    """generate signature to integrity check"""
    if not isinstance(payload, dict):
        raise ValueError
    value = ';'.join(v for _, v in sorted(payload.items()))
    h = hashlib.sha256(value.encode())
    return h.hexdigest()
