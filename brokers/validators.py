from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature
from .dictdb import Transaction


class IsValidTransactionValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        parent = serializer_field.parent
        tran = Transaction(str(value))

        self.exist_validate(tran)
        self.signature_validate(tran, parent.initial_data)
        self.status_validate(tran)

    def exist_validate(self, tran):
        if not tran.exist():
            message = _('transaction code non-existent.')
            raise serializers.ValidationError(message)

    def signature_validate(self, tran, initial_data):
        data = {
            k: v for k, v in initial_data.items()
            if k in tran.payload.keys()
        }
        signature = generate_signature(data)
        if tran.signature != signature:
            message = _('transaction signature is invalid.')
            raise serializers.ValidationError(message)

    def status_validate(self, tran):
        if tran.status != Transaction.STATUS.awaiting:
            message = _('transaction status is %s.' % tran.status)
            raise serializers.ValidationError(message)
