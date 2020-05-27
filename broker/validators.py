from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from broker.services import generate_signature

from .dictdb import Transaction


class TransactionSignatureValidator:

    requires_context = True

    def __init__(self, skip=[]):
        self.skip = skip

    def __call__(self, value, serializer_field):
        tran = Transaction(str(value))
        if tran.exist():
            parent = serializer_field.parent
            data = {
                k: v for k, v in parent.initial_data.items()
                if k not in self.skip}
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
