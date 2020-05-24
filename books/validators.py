import json

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .dictdb import Storage


class TransactionIdValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        db = Storage(request.data['id'])
        if hasattr(db, 'record'):
            message = _('id is a non-existent transaction.')
            raise serializers.ValidationError(message)


class CreditorAndDebtorSameUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        db = Storage(request.data['id'])
        record = json.loads(db['record'])
        if int(record['creditor']) == request.user.id:
            message = _('creditor and debtor are the same user.')
            raise serializers.ValidationError(message)
