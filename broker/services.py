def translate_fk_names(data):
    """ translate foreign keys names """
    field = {
        'creditor': 'creditor_id', 'debtor': 'debtor_id',
        'buyer': 'buyer_id', 'seller': 'seller_id',
    }
    data = {
        **{field[k]: v for k, v in data.items() if k in field.keys()},
        **{k: v for k, v in data.items() if k not in field.keys()}
    }
    return data
