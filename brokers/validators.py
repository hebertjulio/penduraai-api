from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class IsValidTransactionValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        parent = serializer_field.parent
        data = parent.initial_data
        tran = Transaction(str(value))
        IsValidTransactionValidator.exist_validate(tran)
        IsValidTransactionValidator.signature_validate(tran, data)
        IsValidTransactionValidator.status_validate(tran)

    @staticmethod
    def exist_validate(tran):
        if not tran.exist():
            message = _('Transaction non-existent.')
            raise serializers.ValidationError(message)

    @staticmethod
    def signature_validate(tran, initial_data):
        data = {
            k: v for k, v in initial_data.items()
            if k in tran.payload.keys()
        }
        signature = generate_signature(data)
        if tran.signature != signature:
            message = _('Invalid transaction signature.')
            raise serializers.ValidationError(message)

    @staticmethod
    def status_validate(tran):
        if tran.status != Transaction.STATUS.awaiting:
            message = _('Transaction status is %s.' % tran.status)
            raise serializers.ValidationError(message)
