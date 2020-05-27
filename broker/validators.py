from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from broker.services import generate_signature

from .dictdb import Transaction


class TransactionSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        tran = Transaction(str(value))
        parent = serializer_field.parent
        meta = parent.Meta.__dict__
        signature_fields = []
        if 'signature_fields' in meta.keys():
            signature_fields = meta['signature_fields']
        parent = serializer_field.parent
        data = {
            k: v for k, v in parent.initial_data.items()
            if k in signature_fields}
        signature = generate_signature(str(value), data)
        if tran.signature != signature:
            message = _('Transaction signature is invalid.')
            raise serializers.ValidationError(message)


class TransactionCodeExistValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if not tran.exist():
            message = _('Transaction code non-existent.')
            raise serializers.ValidationError(message)
