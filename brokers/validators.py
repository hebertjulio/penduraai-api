from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class TransactionSignatureValidator:

    requires_context = True

    def __init__(self, fields=None):
        if fields is not None:
            if not isinstance(fields, list):
                raise ValueError
        self.fields = fields or []

    def __call__(self, value, serializer_field):
        parent = serializer_field.parent
        data = {
            k: v for k, v in parent.initial_data.items()
            if k in self.fields
        }
        signature = generate_signature(data)
        tran = Transaction(str(value))
        if tran.signature != signature:
            message = _('Transaction signature is invalid.')
            raise serializers.ValidationError(message)


class TransactionValidator:

    def __call__(self, value):
        tran = Transaction(str(value))
        if not tran.exist():
            message = _('Transaction code non-existent.')
            raise serializers.ValidationError(message)
        if tran.status != Transaction.STATUS.awaiting:
            message = _('Transaction status %s.' % tran.status)
            raise serializers.ValidationError(message)
