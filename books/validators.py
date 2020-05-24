import json

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .storages import Transaction


class TransactionIdValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        t = Transaction(request.data['id'])
        if t.exist is None:
            message = _('id is a non-existent transaction.')
            raise serializers.ValidationError(message)


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        t = Transaction(request.data['id'])
        record = json.loads(t.record)
        if int(record['creditor']) == request.user.id:
            message = _('creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
