import json

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .storages import Transaction


class TransactionExistValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        tran = Transaction(request.data['transaction'])
        if not tran.exist():
            message = _('transaction non-existent.')
            raise serializers.ValidationError(message)


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        tran = Transaction(request.data['transaction'])
        data = json.loads(tran.data)
        if int(data['creditor']) == request.user.id:
            message = _('creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
